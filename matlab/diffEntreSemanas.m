% Load the data from the text file
data = dlmread('../datasets/ugr16/june_week2_csv/BPSyPPS_commadecimal.txt');
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

long_periodo = 86400

% Specify the time period
% 1 dia. *1 -> 7 Junio 2016
start_index = -67+long_periodo*3;       % Starting index of the time period

% Select the data within the specified time period
x_period = x(start_index:end_index);
y_period = y(start_index-long_periodo:start_index)./y(start_index:start_index+long_periodo);


% Create the x-y plot
figure;
plot(x_period, y_period, 'b-o');  % Blue line with circles
xlabel('x');
ylabel('y');
title('x-y Plot');
grid on;


% Save the plots (optional)
% saveas(gcf, 'x_y_plot.png');  % Save x-y plot
% saveas(gcf, 'x_z_plot.png');  % Save x-z plot
