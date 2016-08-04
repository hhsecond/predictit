import scrapy, logging, re
regx = re.compile('[0-9]{1,2}\\.\d')

logging.basicConfig(filename='commentary_bot.log', filemode='w', format='%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

def links():
    with open('/home/hhsecond/predictor/project_cricbuz/tabular.txt', 'r') as f:
        default_path = 'http://127.0.0.1:8000/home/hhsecond/cricbuz_data/'
        path = []
        for line in f:
            lis = line.split('==')
            current_path = default_path + '/'.join([lis[3], lis[4], lis[5]]) + '/cricket-scores.html'
            path.append(current_path)
    return list(set(path))

class commentary_fetcher(scrapy.Spider):
    """docstring for commentary_fetcher"""
    name = 'commentary_fetcher'
    allowed_domains = ['127.0.0.1:8000']
    start_urls = links()
    out_text = {}
    temp_out_text = []
    tabular_data = {}
    with open('/home/hhsecond/predictor/project_cricbuz/tabular.txt', 'r') as f:
        for line in f:
            temp = line.split('==')
            tabular_data['/'.join([temp[3], temp[4], temp[5]])] = [temp[11], temp[15]]
    temp_path = '1988/west-indies-in-england/eng-vs-wi-2nd-odi-west-indies-in-england'
    assert (tabular_data[temp_path] == ['ENGLAND', 'WEST INDIES'])



    def parse(self, response):
        logging.debug(response.url)
        body = response.xpath('//text()').extract()
        
        #appending a dummy value to maintain the loop till last bowl
        body.append('0.00')
        
        logging.debug('finding text started')
        ver = 0
        verver = 1
        temp_text = ''
        bowl = []
        checker = 0

        try:
            path = response.url
            path = path.split('/')
            path = '/'.join(path[6:-1])
            t1 = self.tabular_data[path][0]
            t2 = self.tabular_data[path][1]
        except IndexError:
            logging.error('index error:', tabular_data[path])


        for val in body:
            value = val.strip()
            if regx.match(value):
                ver += 1
                #using list for bowl coz if string the value will be overwritten
                bowl.append(value)
            if ver > 0:
                temp_text += val
            if ver > verver:
                #LHS taking second last data from the bowl
                #RHS removing first and last 3 letters which is over
                index = bowl[0]
                backup_index = bowl[0]
                #if loop avoids overlap of commentary to the same bowl for both team
                if checker == 1:
                    index = t1 + ':' + index
                else:
                    index = t2 + ':' + index
                if index == t2 + ':' + '0.1':
                    checker = 1
                    #this will differentiate two teams
                self.temp_out_text.append(index + ' ' + temp_text[:-len(backup_index)])
                bowl.pop(0)
                temp_text = ''
                verver += 1
        self.out_text[response.url] = self.temp_out_text
        self.temp_out_text = []


    def close(self, reason):
        logging.debug('closing spider: ' + reason)
        out_string = ''
        count = 0
        for key, value in self.out_text.items():
            count += 1
            path = key.split('/')
            path = '/home/hhsecond/predictor/project_cricbuz/commentary_out/' + '--'.join(path[6:])
            out_string = '\n'.join(value)
            if out_string:
                with open(path, 'w+') as f:
                    f.write(out_string)
            else:
                pass