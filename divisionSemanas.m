% Load the data from the text file

data = load('../datasets/ugr16/june_week2_csv/BPSyPPS.txt');
data = [data;load('../datasets/ugr16/june_week3_csv/BPSyPPS.txt')];

x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

duracionSemana = 60*60*24*7
duracionDia = 86400

tiempoBase = -67+duracionDia

tiempoActual = duracionDia*3+duracionSemana;

startIndex = tiempoBase;
offsetActual = duracionDia*3;
endIndex = tiempoBase+duracionSemana;

% Select the data within the specified time period
xPeriod = x(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual);
XDates = datetime(xPeriod, 'convertfrom', 'posixtime');
yPeriod = y(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual)./y(startIndex:startIndex+offsetActual);

window_size = 60*15; % Adjust this parameter to control the level of smoothing
smoothedY = movmean(yPeriod, window_size);

% Create the x-y plot
figure;
plot(XDates, smoothedY, 'b-');  % Blue line with circles
xlabel('x');
ylabel('y');
title('x-y Plot');
grid on;    


% Save the plots (optional)
% saveas(gcf, 'x_y_plot.png');  % Save x-y plot
% saveas(gcf, 'x_z_plot.png');  % Save x-z plot
