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
xPoints = x(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual);
yPoints = y(duracionSemana+startIndex:duracionSemana+startIndex+offsetActual);

% Define a range for extrapolation (e.g., predicting traffic for x = 11 to x = 15)
xExtrapolation = xPoints(1)+length(xPoints):xPoints(1)+length(xPoints)+300;


% Perform cubic spline interpolation
splineCoefficients = spline(xPoints, yPoints);

% Use the spline coefficients for extrapolation
yExtrapolation = ppval(splineCoefficients, xExtrapolation);

% Plot the original data and the extrapolated values
plot(xPoints, yPoints, 'o', xExtrapolation, yExtrapolation, '--');
xlabel('xPoints');
ylabel('Traffic Volume');
title('Traffic Forecasting with Spline Extrapolation');
legend('Observed Data', 'Extrapolated Data', 'Location', 'northwest');
grid on;

% Display the extrapolated values
disp('Extrapolated Traffic Volumes:');
disp([xExtrapolation', yExtrapolation']);
