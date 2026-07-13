clear,clc, close all

syms x
fplot(@(x) (x.^2).* cosh(x.^2)- (x.^2).*sinh(x.^2) - 2*(x.^2).*cosh(x).*cos(x) + x.^2, [-20, 20], 'MeshDensity', 1000)
ylim([-100, 100]) % Ajuste esse valor conforme necessário
grid on
