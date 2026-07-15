clear,clc

n_monster = 600;

% n_m = porcentagem, g_m = gold que o monstro da 
n_m(1) = 24.7; g_m(1) = 449;
n_m(2) = 24.7; g_m(2) = 345;
n_m(3) = 13.6; g_m(3) = 345;
n_m(4) = 12.3; g_m(4) = 1209;
n_m(5) = 17.3; g_m(5) = 691;
n_m(6) = 7.4; g_m(6) = 1554;
g_boss = 2073;

% rune + pet input
multiplier = 1 + (1.9+0.15);
add_normal = 8;
add_boss = 12180;
time = 270; 

gold_p_H = ( (sum(((n_m/100)*n_monster).*(g_m + add_normal)) + ...
    (g_boss + add_boss)) *multiplier) *(60/(time/60))

% objetivos

objv(1) = 140e6; % runas de gold
objv(2) = 7319e6; % runas de chest
objv(3) = 70e6; % runas de xp

% tempo q leva pra fzer cada objv
t_objv = objv/gold_p_H