warning('off')
% Step 1: Read data from CSV into a table
data = readtable('../csv/diff_no_attack.csv');

window_size = 898;

variable_to_fit = data.Var1;

% Determine the number of windows
num_windows = floor(length(variable_to_fit)/window_size)-1;

% Initialize arrays to store the parameters
alpha_values = zeros(num_windows, 1);
beta_values = zeros(num_windows, 1);
gamma_values = zeros(num_windows, 1);
delta_values = zeros(num_windows, 1);
attack_value = zeros(num_windows, 1);
% Loop through each window
for i = 0:num_windows
    % Extract the current window
    current_window = variable_to_fit((1+i*window_size):(720+i*window_size));
    
    % Fit the data to a Stable Distribution
    pd1 = fitdist(current_window, 'Stable');
    current_window = variable_to_fit((1+i*window_size):(898+i*window_size));
    pd2 = fitdist(current_window, 'Stable');
    % Store the parameters
    alpha_values(i+1) = pd1.alpha-pd2.alpha;
    beta_values(i+1) = pd1.beta-pd2.beta;
    gamma_values(i+1) = pd1.gam-pd2.gam;
    delta_values(i+1) = pd1.delta-pd2.delta;
    attack_value(i+1) = 0;
end

% Create a table with alpha and beta values
result_table = table(alpha_values, beta_values, gamma_values, delta_values, attack_value);

% Save the table to a CSV file
writetable(result_table, '../csv/alpha_fit_values_no_attack.csv');

%Previous 12min
%Mean Alpha: 1.5217, Standard Deviation Alpha: 0.20864
%Mean Beta: -0.0042575, Standard Deviation Beta: 0.11102
%Mean Gamma: 5222267.6763, Standard Deviation Gamma: 2086933.5073
%Mean Delta: -13544.0857, Standard Deviation Delta: 1672497.5733
%Attack 3min
%Mean Alpha: 1.6192, Standard Deviation Alpha: 0.21752
%Mean Beta: 0.002436, Standard Deviation Beta: 0.32663
%Mean Gamma: 5396507.1338, Standard Deviation Gamma: 10817499.0959
%Mean Delta: 807355.8413, Standard Deviation Delta: 15285729.7153
%Ventana 15min
%Mean Alpha: 1.5231, Standard Deviation Alpha: 0.19637
%Mean Beta: 3.633e-05, Standard Deviation Beta: 0.085633
%Mean Gamma: 5110109.1636, Standard Deviation Gamma: 1891338.7641
%Mean Delta: 52644.525, Standard Deviation Delta: 1051646.3791

% Saco la conclusion de que deberiamos de comparar el alfafit de solo los 3
% minutos, aunque sean pocos... Los 12 minutos anteriores opacan a las 
% posibles anomalias de los 3 minutos de ataque

% Pintamos ->
