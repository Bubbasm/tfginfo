warning('off')
% Step 1: Read data from CSV into a table
data = readtable('../python/ventana_test.csv');

% Make alpha fit for x0_t0, x0_t1, x1_t0, x1_t1, x2_t0, x2_t1
% Step 2: Extract data for x0_t0, x0_t1, x1_t0, x1_t1, x2_t0, x2_t1
x0_t0 = data.x0_t0;
x0_t1 = data.x0_t1;
x1_t0 = data.x1_t0;
x1_t1 = data.x1_t1;
x2_t0 = data.x2_t0;
x2_t1 = data.x2_t1;

% Step 3: Fit data to alpha function
% x0_t0
x0_t0_fit = fitdist(x0_t0, 'Stable');
x0_t0_norm = (x0_t0 - x0_t0_fit.delta)/x0_t0_fit.gam;
x0_t0_norm_fit = fitdist(x0_t0_norm, 'Stable');
% x0_t1
x0_t1_fit = fitdist(x0_t1, 'Stable');
x0_t1_norm = (x0_t1 - x0_t1_fit.delta)/x0_t1_fit.gam;
x0_t1_norm_fit = fitdist(x0_t1_norm, 'Stable');
% x1_t0
x1_t0_fit = fitdist(x1_t0, 'Stable');
x1_t0_norm = (x1_t0 - x1_t0_fit.delta)/x1_t0_fit.gam;
x1_t0_norm_fit = fitdist(x1_t0_norm, 'Stable');
% x1_t1
x1_t1_fit = fitdist(x1_t1, 'Stable');
x1_t1_norm = (x1_t1 - x1_t1_fit.delta)/x1_t1_fit.gam;
x1_t1_norm_fit = fitdist(x1_t1_norm, 'Stable');
% x2_t0
x2_t0_fit = fitdist(x2_t0, 'Stable');
x2_t0_norm = (x2_t0 - x2_t0_fit.delta)/x2_t0_fit.gam;
x2_t0_norm_fit = fitdist(x2_t0_norm, 'Stable');
% x2_t1
x2_t1_fit = fitdist(x2_t1, 'Stable');
x2_t1_norm = (x2_t1 - x2_t1_fit.delta)/x2_t1_fit.gam;
x2_t1_norm_fit = fitdist(x2_t1_norm, 'Stable');

% Write xi_tj_norm to new table
alpha_fit = table(x0_t0_norm, x0_t1_norm, x1_t0_norm, x1_t1_norm, x2_t0_norm, x2_t1_norm);
writetable(alpha_fit, 'ventana_test_norm.csv');

