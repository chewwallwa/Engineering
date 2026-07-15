clear; clc;

% =========================================================================
% PARÂMETROS BASE GLOBAIS (LA.M.E.C) 
% =========================================================================
 % ranger = 1; knight = 0.9; sorcerer = 0.84; priest = 0.9;
aspd_base = 1;

% ranger = 14.375; knight = 16.625; sorcerer = 25.625; priest = 15.175;
base_flat_atk = 14.375;

% ranger = 4%; knight = 2.5%; sorcerer = 5%; priest = 2%;
base_crit_chance = 4/100;

% ranger = 150%;  knight = 140%; sorcerer = 165%; priest = 140;
base_crit_dmg = 150/100; 

% =========================================================================
% DEFINIÇÃO DE EQUIPAMENTOS (MATRIZ DE ATRIBUTOS)
% =========================================================================
eqp(1).slot = 'Arco Imortal';
eqp(1).flat_dmg = 594+144;
eqp(1).dmg_pct = 0;       
eqp(1).phys_dmg_pct = 0;
eqp(1).atk_spd = 19/100;  
eqp(1).crit_chance_flat = 0;
eqp(1).crit_chance_pct = 0;
eqp(1).crit_dmg_pct = 0;
eqp(1).projectile_dmg_pct = 0;

eqp(2).slot = 'Arco Imortal - Decoracoes';
eqp(2).flat_dmg = 0;       
eqp(2).dmg_pct = 0;
eqp(2).phys_dmg_pct = (31+33+78)/100; 
eqp(2).atk_spd = 0.00;
eqp(2).crit_chance_flat = 0;
eqp(2).crit_chance_pct = 0;
eqp(2).crit_dmg_pct = 0;
eqp(2).projectile_dmg_pct = 0;

eqp(3).slot = 'Flecha Imortal';
eqp(3).flat_dmg = 0;
eqp(3).dmg_pct = 49/100;      
eqp(3).phys_dmg_pct = 0;
eqp(3).atk_spd = (44+15)/100;       
eqp(3).crit_chance_flat = 0;
eqp(3).crit_chance_pct = 0;
eqp(3).crit_dmg_pct = 0;
eqp(3).projectile_dmg_pct = 0;

eqp(4).slot = 'Flecha Imortal - Decoracoes';
eqp(4).flat_dmg = 0;       
eqp(4).dmg_pct = 69/100;
eqp(4).phys_dmg_pct = (31+34)/100; 
eqp(4).atk_spd = 0;
eqp(4).crit_chance_flat = 0;
eqp(4).crit_chance_pct = 0;
eqp(4).crit_dmg_pct = 0;
eqp(4).projectile_dmg_pct = 0;

eqp(5).slot = 'Amuleto';
eqp(5).flat_dmg = 0;
eqp(5).dmg_pct = 0;
eqp(5).phys_dmg_pct = 0;
eqp(5).atk_spd = 0;
eqp(5).crit_chance_flat = 0;
eqp(5).crit_chance_pct = 0;
eqp(5).crit_dmg_pct = 0;
eqp(5).projectile_dmg_pct = 0;

eqp(6).slot = 'Amuleto - deco';
eqp(6).flat_dmg = 0;
eqp(6).dmg_pct = 0;
eqp(6).phys_dmg_pct = 0;
eqp(6).atk_spd = 0;
eqp(6).crit_chance_flat = 0;
eqp(6).crit_chance_pct = 0;
eqp(6).crit_dmg_pct = 0;
eqp(6).projectile_dmg_pct = 0;

eqp(7).slot = 'Brinco';
eqp(7).flat_dmg = 288;
eqp(7).dmg_pct = 0;
eqp(7).phys_dmg_pct = 0;
eqp(7).atk_spd = 0;
eqp(7).crit_chance_flat = 0;
eqp(7).crit_chance_pct = 0;
eqp(7).crit_dmg_pct = 0;
eqp(7).projectile_dmg_pct = 0;

eqp(8).slot = 'Brinco - deco';
eqp(8).flat_dmg = 0;
eqp(8).dmg_pct = 0;
eqp(8).phys_dmg_pct = 0;
eqp(8).atk_spd = 0;
eqp(8).crit_chance_flat = 0;
eqp(8).crit_chance_pct = 0;
eqp(8).crit_dmg_pct = 0;
eqp(8).projectile_dmg_pct = 0;

eqp(9).slot = 'Anel';
eqp(9).flat_dmg = 0;
eqp(9).dmg_pct = 0;
eqp(9).phys_dmg_pct = 0;
eqp(9).atk_spd = 11/100;
eqp(9).crit_chance_flat = 0;
eqp(9).crit_chance_pct = 0;
eqp(9).crit_dmg_pct = 0;
eqp(9).projectile_dmg_pct = 0;

eqp(10).slot = 'Anel - deco';
eqp(10).flat_dmg = 0;
eqp(10).dmg_pct = 0;
eqp(10).phys_dmg_pct = 0;
eqp(10).atk_spd = 0;
eqp(10).crit_chance_flat = 0;
eqp(10).crit_chance_pct = 0;
eqp(10).crit_dmg_pct = 0;
eqp(10).projectile_dmg_pct = 0;

eqp(11).slot = 'Bracelete';
eqp(11).flat_dmg = 0;
eqp(11).dmg_pct = 0;
eqp(11).phys_dmg_pct = 0;
eqp(11).atk_spd = 0;
eqp(11).crit_chance_flat = 0;
eqp(11).crit_chance_pct = 0;
eqp(11).crit_dmg_pct = 0;
eqp(11).projectile_dmg_pct = 0;

eqp(12).slot = 'Bracelete - deco';
eqp(12).flat_dmg = 0;
eqp(12).dmg_pct = 0;
eqp(12).phys_dmg_pct = 0;
eqp(12).atk_spd = 0;
eqp(12).crit_chance_flat = 0;
eqp(12).crit_chance_pct = 0;
eqp(12).crit_dmg_pct = 0;
eqp(12).projectile_dmg_pct = 0;

eqp(13).slot = 'Runas';
eqp(13).flat_dmg = 12;
eqp(13).dmg_pct = 60/100;
eqp(13).phys_dmg_pct = 0; 
eqp(13).atk_spd = 21/100;
eqp(13).crit_chance_flat = 0;
eqp(13).crit_chance_pct = 0;
eqp(13).crit_dmg_pct = 0;
eqp(13).projectile_dmg_pct = 0;

eqp(14).slot = 'Skills';
eqp(14).flat_dmg = 3;
eqp(14).dmg_pct = 0;
eqp(14).phys_dmg_pct = 0; 
eqp(14).atk_spd = ((4*8) + (10*5) + (10*6))/100;
eqp(14).crit_chance_flat = 0;
eqp(14).crit_chance_pct = (20*8)/100;
eqp(14).crit_dmg_pct = (13*3)/100;
eqp(14).projectile_dmg_pct = (20*15)/100;

eqp(15).slot = 'Armaduras';
eqp(15).flat_dmg = 2;
eqp(15).dmg_pct = 0;
eqp(15).phys_dmg_pct = 0; 
eqp(15).atk_spd = (11+17)/100;
eqp(15).crit_chance_flat = 0;
eqp(15).crit_chance_pct = 0;
eqp(15).crit_dmg_pct = 0;
eqp(15).projectile_dmg_pct = 0;

% =========================================================================
% PROCESSAMENTO COMPUTACIONAL: SEGREGAÇÃO POR ORIGEM
% =========================================================================
% Definição dos índices de mapeamento estrutural
idx_eqp   = [1:12, 15];
idx_runas = 13;
idx_skill = 14;

% Somatório Flat Total unificado (Dano Bruto independe de Produto)
tot_flat = base_flat_atk + sum([eqp.flat_dmg]);

tot_crit_chance_flat = sum([eqp.crit_chance_flat]);
tot_crit_chance_pct  = sum([eqp.crit_chance_pct]);
tot_crit_dmg_pct     = sum([eqp.crit_dmg_pct]);

% 1. Produto Triplo: Multiplicadores de Dano (%)
mult_dmg_eqp   = 1 + sum([eqp(idx_eqp).dmg_pct]);
mult_dmg_runas = 1 + sum([eqp(idx_runas).dmg_pct]);
mult_dmg_skill = 1 + sum([eqp(idx_skill).dmg_pct]);
fator_dmg_global = mult_dmg_eqp * mult_dmg_runas * mult_dmg_skill;

% Produto Triplo: Multiplicadores de Dano Físico (%)
mult_phys_eqp   = 1 + sum([eqp(idx_eqp).phys_dmg_pct]);
mult_phys_runas = 1 + sum([eqp(idx_runas).phys_dmg_pct]);
mult_phys_skill = 1 + sum([eqp(idx_skill).phys_dmg_pct]);
fator_phys_global = mult_phys_eqp * mult_phys_runas * mult_phys_skill;

% Produto Triplo: Multiplicadores de Dano de Projétil (%)
mult_proj_eqp   = 1 + sum([eqp(idx_eqp).projectile_dmg_pct]);
mult_proj_runas = 1 + sum([eqp(idx_runas).projectile_dmg_pct]);
mult_proj_skill = 1 + sum([eqp(idx_skill).projectile_dmg_pct]);
fator_proj_global = mult_proj_eqp * mult_proj_runas * mult_proj_skill;

% 2. Produto Triplo: Extração de Velocidade de Ataque (ASPD)
mult_aspd_eqp   = 1 + sum([eqp(idx_eqp).atk_spd]);
mult_aspd_runas = 1 + sum([eqp(idx_runas).atk_spd]);
mult_aspd_skill = 1 + sum([eqp(idx_skill).atk_spd]);

aspd_final = aspd_base * mult_aspd_eqp * mult_aspd_runas * mult_aspd_skill; 
aspd_capped = min(aspd_final, 6.0); 

% 3. Resolução de Crítico
final_crit_chance = (base_crit_chance + tot_crit_chance_flat) * (1 + tot_crit_chance_pct);
final_crit_dmg = base_crit_dmg + tot_crit_dmg_pct;
fator_critico = 1 + (final_crit_chance * (final_crit_dmg - 1));

% 4. Frequência de Ataque 
theo_atk_freq = 1 / (aspd_final / 60); 
if aspd_final >= 6.0
    real_atk_freq = 1 / 0.217; 
else
    real_atk_freq = aspd_capped; 
end

% 5. Dano por Acerto e DPS
attack_real = tot_flat * fator_dmg_global * fator_phys_global * fator_proj_global;
in_game_dps = (tot_flat * fator_dmg_global) * aspd_final * fator_critico;
real_dps = attack_real * real_atk_freq * fator_critico; 

% =========================================================================
% OUTPUT DE DADOS (LA.M.E.C)
% =========================================================================
fprintf('=== in game ===\n');
fprintf('Atack Damage               : %.2f\n', tot_flat * fator_dmg_global); 
fprintf('Atack Speed                : %.4f\n', aspd_final);
fprintf('Critical Chance            : %.2f %%\n', final_crit_chance * 100);
fprintf('Critical Damage %%          : %.2f %%\n', final_crit_dmg * 100);
fprintf('DPS                        : %.2f\n', in_game_dps);
fprintf('Physical Damage multiplier : %.0f %%\n', 100 * (fator_phys_global - 1));
fprintf('\n');
fprintf('=== calculated ===\n');
fprintf('Theoretical Atack Frequency: %.4f atk/s\n', theo_atk_freq);
fprintf('Capped Atack speed         : %.4f\n', aspd_capped);
fprintf('Real Atack Frequency       : %.4f atk/s\n', real_atk_freq);
fprintf('Damage Per hit             : %.2f\n', attack_real);
fprintf('Real DPS                   : %.2f\n', real_dps);
fprintf('=================================\n');