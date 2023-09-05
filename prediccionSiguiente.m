% Load the data from the text file
data1 = dlmread('../datasets/ugr16/june_week2_csv/BPSyPPS_commadecimal.txt');
data2 = dlmread('../datasets/ugr16/june_week3_csv/BPSyPPS_commadecimal.txt');
x = cat(1,data1(:, 1), data2(:, 1));
y = cat(1,data1(:, 2), data2(:, 2));
z = cat(1,data1(:, 3), data2(:, 3));

duracionSemana = 60*60*24*7
duracionDia = 86400

tiempoBase = -67+duracionDia

tiempoActual = duracionDia*3+duracionSemana;

startIndex = tiempoBase;
offsetActual = duracionDia*3;
endIndex = tiempoBase+duracionSemana;

% Select the data within the specified time period
xPeriod = x(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual);
yPeriod = y(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual)./y(startIndex:startIndex+offsetActual);

window_size = 60*60; % Adjust this parameter to control the level of smoothing
smoothedY = movmean(yPeriod, window_size);

% Create the x-y plot
figure;
plot(xPeriod, smoothedY, 'b-');  % Blue line with circles
xlabel('x');
ylabel('y');
title('x-y Plot');
grid on;


% Save the plots (optional)
% saveas(gcf, 'x_y_plot.png');  % Save x-y plot
% saveas(gcf, 'x_z_plot.png');  % Save x-z plot
