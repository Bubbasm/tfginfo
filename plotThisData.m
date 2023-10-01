% Load the data from the text file
data = load('../datasets/ugr16/june_week2_csv/BPSyPPS.txt');

x = data(:, 1);
y = data(:, 2);
z = data(:, 3);


showDays = 5
start_index = 1;          % Starting index of the time period
end_index = start_index + 86400*showDays; % Ending index of the time period

% Select the data within the specified time period
x_period = x(start_index:end_index);
XDates = datetime(x_period, 'convertfrom', 'posixtime');
y_period = y(start_index:end_index);
z_period = z(start_index:end_index);

window_size = 60*15; % Adjust this parameter to control the level of smoothing
smoothedY = movmean(y_period, window_size);
smoothedZ = movmean(z_period, window_size);

% Create the x-y plot
figure;
plot(XDates, smoothedY, 'b-');  % Blue line
xlabel('x');
ylabel('y');
title('Bitrate');
grid on;
hold on;
xline([1:(showDays+1)])
figure;
plot(XDates, smoothedZ, 'r-');  % Red line
xlabel('x');
zlabel('z');
title('Packet rate');
grid on;
hold on;
xline([1:(showDays+1)])
