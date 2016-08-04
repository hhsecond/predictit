function plotdata(x,y)
    
    data = load('tabular.txt');
    x = data(:, [2,3]);
    y = data(:, 1);

    figure;hold on;
    z = x * 10;
    ri = rand(length(y), 1) .* randi([-3, 3], length(y), 1);
    rj = rand(length(y), 1) .* randi([-3, 3], length(y), 1);
    z(:, 1) = z(:, 1) .+ ri;
    z(:, 2) = z(:, 2) .+ rj;

    pos = find(y==1);
    neg = find(y==0);

    xlabel('ground');
    ylabel('toss result');

    %plot(z(pos,1), z(pos,2), 'k+', 'LineWidth', 2);
    plot(z(neg,1), z(neg,2), 'ko', 'MarkerFaceColor', 'y');