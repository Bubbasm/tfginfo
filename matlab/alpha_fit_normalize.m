warning('off')
% Step 1: Read data from CSV into a table
data1 = readtable('../csv/diff_attack.csv');
data2 = readtable('../csv/diff_no_attack.csv');

window_size = 898;

d1 = data1.Var1;
d2 = data2.Var1;

% Determine the number of windows
num_windows = floor(length(d1)/window_size);

% Initialize arrays to store the parameters
alpha_values = zeros(num_windows*2, 1);
beta_values = zeros(num_windows*2, 1);
gamma_values = zeros(num_windows*2, 1);
delta_values = zeros(num_windows*2, 1);
attack_value = zeros(num_windows*2, 1);
% Loop through each window
for i = 1:num_windows
    % Extract the current window
    current_window = d1((1+(i-1)*window_size):(720+(i-1)*window_size));

    % Fit the data to a Stable Distribution
    try
       pd1 = fitdist(current_window, 'Stable');
    catch exception
       continue
    end
    cw1 = d1((720+(i-1)*window_size):(898+(i-1)*window_size));
    cw2 = d2((720+(i-1)*window_size):(898+(i-1)*window_size));
    % substract delta and divide by gamma
    if (isinf((cw1(1)-pd1.delta)/pd1.gam) || isinf((cw2(1)-pd1.delta)/pd1.gam))
        continue
    end
    cw1 = (cw1 - pd1.delta) / pd1.gam;
    cw2 = (cw2 - pd1.delta) / pd1.gam;
    try
       pd21 = fitdist(cw1, 'Stable');
       pd22 = fitdist(cw2, 'Stable');
    catch exception
       continue
    end
    % Store the parameters
    alpha_values(i) = pd21.alpha;
    beta_values(i) = pd21.beta;
    gamma_values(i) = pd21.gam;
    delta_values(i) = pd21.delta;
    attack_value(i) = 1;
    alpha_values(num_windows+i) = pd22.alpha;
    beta_values(num_windows+i) = pd22.beta;
    gamma_values(num_windows+i) = pd22.gam;
    delta_values(num_windows+i) = pd22.delta;
    attack_value(num_windows+i) = 0;
end

% Create a table with alpha and beta values
result_table = table(alpha_values, beta_values, gamma_values, delta_values, attack_value);

% Save the table to a CSV file
writetable(result_table, '../csv/alpha_fit_normalized.csv');
