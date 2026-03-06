% %% 1 cell =================================================================
% %% ------------------------------------------------------------------------
% % clear, clc, close all
% % INPUT 
% E = 200e9;                              % Young's modulus [Pa]
% rho = 7800;                             % density [kg/m^3]
% A = 0.05;                               % cross section area [m^2]
% d = 0.01;                               % distance between masses [m]
% 
% % ANALYSIS 
% k = E * A / d;                          % spring constant
% m = rho * A * d;                        % mass
% 
% % -------------------------------------------------------------------------
% % nondimensional wavenumber
% mu = linspace(-6*pi, 6*pi, 1e3);
% % "obtained by imposing a range of wavenumbers and solving for frequency"  
% 
% % dispersion relation
% Omega = sqrt( 2*(1 - cos(mu)) );        % nondimensional frequency (6)
% 
% % -------------------------------------------------------------------------
% figure %
% plot(mu/pi, Omega, 'k',LineWidth=2);
% title('Fig. 2: Dispersion relation for the 1D spring-mass lattice')
% xlabel('\mu/\pi'); ylabel('\Omega')
% axis([min(mu/pi) max(mu/pi) 0 2.3])
% 
% % -------------------------------------------------------------------------
% % natural frequency \omega_0
% w0 = sqrt(k / m);                       
% 
% % phase velocity (9)
% c_ph = w0*(abs(sin(mu/2))./abs(mu/2))*d; 
% 
% % -------------------------------------------------------------------------
% figure % 
% plot(mu/pi, (c_ph/(d*w0)), 'k',LineWidth=2)
% title('Fig. 3: Phase velocity of the 1D spring-mass lattice')
% xlabel('\mu/\pi'); ylabel('c_{ph}/(d\omega_0)')
% axis([min(mu/pi) max(mu/pi) 0 1.2])
% 
% %% ------------------------------------------------------------------------
% % clear, clc; close all
% 
% % nondimensional frequency
% Omega = linspace(0, 3, 1e3);
% 
% % inverted dispersion relation for finding wave number
% mii = acos(1 - ((Omega.^2)/2));
% % " The amount of attenuation encountered within the stop band can be      
% % quantified by solving the dispersion relation at a given frequency in 
% % terms of the wavenumber"
% 
% % -------------------------------------------------------------------------
% figure %
% hold on
% plot(imag(mii),Omega, 'k',LineWidth=2,LineStyle='--')
% plot(real(mii),Omega, 'k',LineWidth=2,LineStyle='-')
% title({'Fig. 4: Dispersion relation showing real (solid line) and imaginary'; ...
%     ' (dashed line) parts of propagation constant'})
%  ylabel('\Omega')
% 
% %% full system ============================================================
% %% ------------------------------------------------------------------------
% clear, clc; close all

% INPUT
E = 200e9;                              % Young's modulus [Pa]
rho = 7800;                             % density [kg/m^3]
A = 0.05;                               % cross-sectional area [m^2]
d = 0.01;                               % distance between masses [m]
n = 100;                                % number of masses

k = E * A / d;                          % spring constant
m = rho * A * d;                        % masses
f = [10,1];                             % [force, node] in [N] one line per force

% -------------------------------------------------------------------------
% mass global matrix 
M = m * eye(n);        

% stiffness global matrix 
K = zeros(n);                           % pre-allocation
for i = 1:n-1
    ke = k * [ 1, -1;                   % element stiffness matrix
              -1,  1];
    K(i:i+1, i:i+1) = K(i:i+1, i:i+1) + ke;
end

% applied force 
F = zeros(n,1);
for i = 1:size(f,1)
    F(f(i,2)) = f(i,1);
end

% -------------------------------------------------------------------------
% eigenproblem
[a_vet, a_val] = eig(K, M);             % solve eigenvalue problem
omega = sqrt(diag(a_val));              % natural frequencies

Omega = linspace(0, 2.5, 1e4);          % nondimensional frequency
w0 = sqrt(k / m);                       % omega_0 natural frequency
% resp = zeros(length(Omega), 1);         % harmonic response of the last mass

for i = 1:length(Omega)
    omega = Omega(i) * w0;              % temporal frequency
    x = (K - M * omega^2) \ F;          % harmonic response
    resp(i) = abs(x(end));              % displacement of the *last mass
end
% 
% % [M]{u_n^..} + [K]{u_n} = {F}
% % since the response is harmonic, apply the known response {u_n} = {A_n}sin(omega*t)
% % [K - omega^2 * M]{A_n} = {F}
% % "det(K - omega^2 * M)" <=> eig(K, M) for a_vet and a_val
% % "F / (K - M * omega^2)" for the harmonic response
% % see Petyt - introducttion to FEM section 3.1 (2nd edition)
% 
% % -------------------------------------------------------------------------
% figure %
% semilogy(Omega, resp / abs(nonzeros(F)), 'k', 'LineWidth', 2);
% xlabel('\Omega'); ylabel('u_N / f_0');
% title('Fig. 5: Harmonic response of the last mass');
% 
% % -------------------------------------------------------------------------
% figure %
% cont = 1;
% for Omegai = [1.99, 2.001, 2.01, 2.1]
%     omega = Omegai * w0;                % temporal frequency
%     x = (K - M * omega^2) \ F;          % harmonic response
%     resp2(:) = x(:);                    % displacement of the *last mass
%     resp2 = resp2/max(max(resp2));
% 
%     subplot(2,2,cont)
%     plot(1:n,resp2, '-ko','MarkerSize',3,'MarkerFaceColor',[0,0,0],LineWidth=0.1);
%     axis([0 n min(resp2)-0.5 max(resp2)+0.5])
%     cont = cont + 1;
% end
% sgtitle({'Fig. 6: Dynamic deformed shapes for a lattice of N=100';...
%     ' masses at \Omega=1.99, \Omega=2.001, \Omega=2.01, \Omega=2.1'})
% % -------------------------------------------------------------------------
% 
% mu = linspace(0, pi, 1000);  % continumn wavenumber (IBZ)
% Omega = sqrt(2*(1 - cos(mu)));
% 
% % discrete Wavenumbers (IBZ) 
% mu_n = (0:n-1) * (pi) / n; % (10)
% Omega_n = sqrt(2*(1 - cos(mu_n))); % (11)
% % Here, $Nd$ is the total length of the finite string Spectral resolution
% % $\Delta \mu = \frac{2\pi}{Nd}$ equals how many different wavenumbers "fit" in the finite system
% % ps.: "mu_n/pi" on the scatter, mu_n is the x coordinate of each natural
% % frequency of the system, (Eq. 10) adapted to the IBZ
% 
% % PLOT
% figure
% hold on
% plot(mu/pi, Omega, 'k', 'LineWidth', 2)                   % Curva da cadeia infinita
% scatter(mu_n/pi, Omega_n, 100, 'k')              % Frequências naturais do sistema finito
% title('Fig. 7: Natural frequencies of a finite, free-free lattice')
% xlabel('\mu/\pi')
% ylabel('\Omega')
% axis([0 1 0 2.25])

% %% DIATOMIC LATTICE =======================================================
% clear; clc; close all
% 
% k  = 1;                                  
% m1 = 1;                                 
% m2 = 2 * m1;                            
% 
% % -------------------------------------------------------------------------
% % Mass matrix of the unit cell
% M =      [ m2,  0; 
%             0, m1];
% 
% % Local stiffness matrices
% K0  = k* [  2, -1; 
%            -1,  2];                    % internal interactions
% Km1 = k* [  0, -1;
%             0,  0];                    % interaction with previous cell (u_2n-1)
% Kp1 = k* [  0,  0;
%            -1,  0];                    % interaction with next cell (u_2n+2)
% % U = k/2(u_2n - u_2n-1) + k/2(u_2n+1 - u_2n) + k/2(u_2n+2 - u_2n+1)
% % do the stiffness matrix and then break it for the DOFs of the cell, and
% % interaction with others, [km1]{u_2n-1,u_2n}, [kp1]{u_2n+1, u_2n+2}
% % there is only the contribution of the stiffness on the masses of the cell
% 
% % -------------------------------------------------------------------------
% mu = linspace(0, 4*pi, 1000);           % (IBZ)
% Omega = zeros(2, length(mu));           % fo the two braches
% for i = 1:length(mu)
%     e_m1  = exp(-1 * 1i * mu(i));
%     e_0   = exp( 0 * 1i * mu(i));
%     e_p1  = exp( 1 * 1i * mu(i));
% 
%     K_mu = Km1*e_m1   +   K0*e_0   +   Kp1*e_p1;
% 
%     % Solve eigenvalue problem
%     omega2 = eig(K_mu, M);
%     Omega(:, i) = sort(sqrt(real(omega2)));
% end
% 
% % -------------------------------------------------------------------------
% figure
% hold on
% plot(mu/pi, Omega(1,:), 'k', 'LineWidth', 2)    % Acoustic branch
% plot(mu/pi, Omega(2,:), 'k--', 'LineWidth', 2)  % Optical branch
% xlabel('\mu/\pi'); ylabel('\Omega')
% title('Fig. 9: Dispersion curves of the 1D diatomic spring-mass lattice')
% axis([0 1 0 2])

%% TRITOMIC LATTICE =======================================================
clear; clc; close all

k  = 1;
m1 = 1;
m2 = 2;
m3 = 1;

n = 10;  

% Mass matrix (diagonal)
M = diag([m1, m2, m3]);

% Internal stiffness matrix K0 (ligações internas da célula)
K0 = k * [  2, -1,  0;
           -1,  2, -1;
            0, -1,  2];

% Interação com célula anterior: ligação entre u3^(n-1) e u1^(n)
Km1 = k * [ 0,  0,  0;
            0,  0,  0;
           -1,  0,  0 ];  % reação da mola entre u1 e u3 (posição (3,1))

% Interação com próxima célula: mesma ligação (mas transposta)
Kp1 = k * [ 0,  0, -1;
            0,  0,  0;
            0,  0,  0 ];  % reação da mola entre u3 e u1 (posição (1,3))

mu = linspace(0, pi, 1000);
Omega = zeros(3, length(mu));

for i = 1:length(mu)
    e_m1 = exp(-1i * mu(i));
    e_0  = 1;
    e_p1 = exp( 1i * mu(i));

    K_mu = Km1 * e_m1 + K0 + Kp1 * e_p1;

    omega2 = eig(K_mu, M);
    Omega(:, i) = sort(sqrt(real(omega2)));
end

% discrete Wavenumbers (IBZ) 

syms W
m1*m2*m3*W^6 - (2*k *(m1*m3 + m1*m2+ m2*m3))*W^4 + (3*k)*(m1+m2+m3)*W^2 - 2*k(1-cos(1))

figure
hold on
plot(mu/pi, Omega(1,:), 'k', 'LineWidth', 2)
plot(mu/pi, Omega(2,:), 'k--', 'LineWidth', 2)
plot(mu/pi, Omega(3,:), 'k-.', 'LineWidth', 2)
% scatter(mu_n/pi, Omega_n, 100, 'k')              % Frequências naturais do sistema finito
xlabel('\mu/\pi'); ylabel('\Omega')
title('Dispersion curves of the 1D triatomic spring-mass lattice')
axis([0 1 0 max(Omega(:))*1.1])

%% 

% E = 200e9;                              % Young's modulus [Pa]
% rho = 7800;                             % density [kg/m^3]
% A = 0.05;                               % cross-sectional area [m^2]
% d = 0.01;                               % distance between masses [m]
% n = 100;                                % number of masses
% 
% k = E * A / d;                          % spring constant
% m = rho * A * d;                        % masses
% f = [10,1];                             % [force, node] in [N] one line per force
% 
% % Mass matrix (diagonal)
% M = diag([m1, m2, m3])* eye(n);
% 
% % Internal stiffness matrix K0 (ligações internas da célula)
% K0 = k * [  2, -1,  0;
%            -1,  2, -1;
%             0, -1,  2];
% 
% % Interação com célula anterior: ligação entre u3^(n-1) e u1^(n)
% Km1 = k * [ 0,  0,  0;
%             0,  0,  0;
%            -1,  0,  0 ];  % reação da mola entre u1 e u3 (posição (3,1))
% 
% % Interação com próxima célula: mesma ligação (mas transposta)
% Kp1 = k * [ 0,  0, -1;
%             0,  0,  0;
%             0,  0,  0 ];  % reação da mola entre u3 e u1 (posição (1,3))







