% Load the data from the text file
data = dlmread('../datasets/ugr16/june_week2_csv/BPSyPPS_commadecimal.txt');
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

% Specify the time period
% 1 dia. *1 -> 7 Junio 2016
start_index = -67+86400*3;          % Starting index of the time period
end_index = start_index + 86400; % Ending index of the time period

% Select the data within the specified time period
x_period = x(start_index:end_index);
y_period = y(start_index:end_index);
z_period = z(start_index:end_index);

% Create the x-y plot
figure;
subplot(2, 1, 1);
plot(x_period, y_period, 'b-o');  % Blue line with circles
xlabel('x');
ylabel('y');
title('x-y Plot');
grid on;

% Create the x-z plot
subplot(2, 1, 2);
plot(x_period, z_period, 'r-s');  % Red line with squares
xlabel('x');
ylabel('z');
title('x-z Plot');
grid on;

% Adjust spacing between subplots
spacing = 0.05;
subplot(2, 1, 1);
pos = get(gca, 'Position');
pos(4) = pos(4) - spacing;
set(gca, 'Position', pos);

subplot(2, 1, 2);
pos = get(gca, 'Position');
pos(2) = pos(2) + spacing;
set(gca, 'Position', pos);


% Save the plots (optional)
% saveas(gcf, 'x_y_plot.png');  % Save x-y plot
% saveas(gcf, 'x_z_plot.png');  % Save x-z plot
