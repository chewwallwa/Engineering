% 3D Truss Finite Element Analysis - Full Stabilized Version
clc; clear; close all;

%% --- 1. PARAMETERS ---
a = 150;     
h = 2000;    
E = 2.1e5;   
A = 400;     
rho = 7850;  

%% --- 2. GEOMETRY (NODES) ---
% Based on parametric formulas
nodes = zeros(24, 3);
nodes(1:4,:) = [-1000,-1000,0; -1000,1000,0; 1000,1000,0; 1000,-1000,0];

for i = 1:3
    base = ((i-1)*4)+1 : ((i-1)*4)+4;
    next = (i*4)+1 : (i*4)+4;
    offset = [a,a,h; a,-a,h; -a,-a,h; -a,a,h];
    nodes(next,:) = nodes(base,:) + offset;
end

% Top and Auxiliary Nodes
nodes(17:20,:) = nodes(13:16,:) + [a,a,h; a,-a,h; -a,-a,h; -a,a,h];
nodes(21,:) = [0, -2000, nodes(20,3)];
nodes(23,:) = [0, 2000, nodes(20,3)];
nodes(22,1:2) = [(nodes(18,1)+nodes(19,1))/2, nodes(18,2)];
nodes(22,3) = nodes(17,3) + abs(nodes(19,1)-nodes(18,1));
nodes(24,1:2) = [(nodes(20,1)+nodes(17,1))/2, nodes(20,2)];
nodes(24,3) = nodes(22,3);

%% --- 3. CONNECTIVITY (ELEMENTS) ---
%
conn = [1,5; 2,6; 3,7; 4,8; 1,8; 5,4; 4,7; 3,8; 2,7; 3,6; 1,6; 2,5;
        5,9; 6,10; 7,11; 8,12; 5,12; 8,9; 5,10; 6,9; 6,11; 7,10; 8,11; 7,12;
        9,13; 10,14; 11,15; 12,16; 12,13; 9,16; 9,14; 10,13; 10,15; 11,14; 11,16; 12,15;
        14,18; 15,19; 16,20; 13,17; 13,18; 14,19; 15,20; 16,17; 17,18; 20,19; 20,17; 18,19;
        22,24; 18,22; 19,22; 20,24; 17,24; 20,21; 17,21; 19,23; 18,23; 22,23; 24,21; 17,22;
        5,8; 5,6; 7,8; 6,7; 11,12; 10,11; 9,10; 9,12; 14,15; 15,16; 13,14; 13,16;
        14,17; 13,20; 16,19; 15,18; 19,24];

num_nodes = size(nodes, 1);
num_elements = size(conn, 1);
num_dof = 3 * num_nodes;

%% --- 4. CALCULATION ENGINE ---
K = zeros(num_dof); M = zeros(num_dof); F = zeros(num_dof, 1);

% Applying Loads
F(3*21) = -1e4; F(3*23) = -1e4; 

% Global Assembly
for i = 1:num_elements
    n = conn(i,:);
    L = norm(nodes(n(2),:) - nodes(n(1),:));
    d = (nodes(n(2),:) - nodes(n(1),:)) / L;
    
    tau = [d, zeros(1,3); zeros(1,3), d];
    k_el = (E*A/L) * [1, -1; -1, 1];
    idx = [3*n(1)-2:3*n(1), 3*n(2)-2:3*n(2)];
    
    K(idx, idx) = K(idx, idx) + tau' * k_el * tau;
    
    % Stable Lumped Mass Matrix for EIG
    m_half = (rho * A * L) / 2;
    M(3*n(1)-2:3*n(1), 3*n(1)-2:3*n(1)) = M(3*n(1)-2:3*n(1), 3*n(1)-2:3*n(1)) + eye(3)*m_half;
    M(3*n(2)-2:3*n(2), 3*n(2)-2:3*n(2)) = M(3*n(2)-2:3*n(2), 3*n(2)-2:3*n(2)) + eye(3)*m_half;
end

% Boundary Conditions (Fixed Base: Nodes 1-4)
fixed_dofs = 1:12; 
free_dofs = setdiff(1:num_dof, fixed_dofs);

% Displacement Solution (Step 5)
U = zeros(num_dof, 1);
U(free_dofs) = K(free_dofs, free_dofs) \ F(free_dofs);

% Frequency Analysis (Step 4)
[~, D] = eig(K(free_dofs, free_dofs), M(free_dofs, free_dofs));
nat_freqs = sort(sqrt(abs(diag(D))) / (2*pi));

%% --- 5. VECTORIZED POST-PROCESSING ---
d_vec = nodes(conn(:,2),:) - nodes(conn(:,1),:);
L_vec = sqrt(sum(d_vec.^2, 2));
dir_cosines = d_vec ./ L_vec;

U1 = [U(3*conn(:,1)-2), U(3*conn(:,1)-1), U(3*conn(:,1))];
U2 = [U(3*conn(:,2)-2), U(3*conn(:,2)-1), U(3*conn(:,2))];

% Internal Forces
axial_stresses = (E ./ L_vec) .* sum(dir_cosines .* (U2 - U1), 2);
axial_forces = axial_stresses .* A;

%% --- 6. TABLES ---
fprintf('\nTABLE 1: NODAL DISPLACEMENTS [m]\n');
disp([(1:num_nodes)', reshape(U, 3, [])']);

fprintf('\nTABLE 2: INTERNAL AXIAL FORCES [N]\n');
status = char(repmat('T', num_elements, 1)); status(axial_forces < 0) = 'C';
for i = 1:num_elements
    fprintf('El %2d: %12.2f [%c]\n', i, abs(axial_forces(i)), status(i));
end

fprintf('\nTABLE 3: NATURAL FREQUENCIES [Hz]\n');
disp(nat_freqs(1:min(10, end)));

%% --- 7. PLOT ---
figure('Color', 'w'); hold on; axis equal; view(-37, 25); grid on;

map_pts = 256;
base_colors = [0 0 1; 1 1 1; 1 0 0]; 
bwr_map = interp1([-1 0 1], base_colors, linspace(-1, 1, map_pts));
colormap(bwr_map);

force_limit = max(abs(axial_forces));
if force_limit == 0, force_limit = 1; end
caxis([-force_limit, force_limit]);
cb = colorbar; ylabel(cb, 'Axial Force (N) [Blue: Comp | Red: Tens]');

scale = 0.1 * max(max(nodes)-min(nodes)) / max(abs(U));

for i = 1:num_elements
    n = conn(i,:); p = nodes(n,:);
    u = [U(3*n-2), U(3*n-1), U(3*n)] * scale;
    
    % Map force to colormap index
    c_idx = round((axial_forces(i) + force_limit) / (2*force_limit) * (map_pts-1)) + 1;
    c_idx = max(1, min(map_pts, c_idx));
    
    % Reference dashed structure
    plot3(p(:,1), p(:,2), p(:,3), '-.', 'Color', [0.8 0.8 0.8]);
    
    % Deformed structure with continuous BWR color
    plot3(p(:,1)+u(:,1), p(:,2)+u(:,2), p(:,3)+u(:,3), ...
          'Color', bwr_map(c_idx,:), 'LineWidth', 2.5);
end
title('3D Tower Analysis - Force Gradient (Blue: Compression, Red: Tension)');
