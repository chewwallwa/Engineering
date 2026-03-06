clear; clc;

% Criando personagens
% (nome, vida, dano, defesa)
Thierry = Personagem('Thierry', 30, 30, 5);
monstro = Personagem('Monstro', 100, 20, 7);

% Mostrando status inicial
disp('--- STATUS INICIAL ---');
Thierry.mostrarStatus();
monstro.mostrarStatus();
disp('----------------------');

% Simulando batalha
[Thierry, monstro] = luta(Thierry, monstro);

% % Simulando batalha
% while heroi.Vida > 0 && monstro.Vida > 0
%     [heroi, monstro] = heroi.atacar(monstro);
% 
%     if monstro.Vida > 0
%         [monstro, heroi] = monstro.atacar(heroi);
%     end
% 
%     pause(1); 
% end

% Mostrando status final
disp('--- STATUS FINAL ---');
Thierry.mostrarStatus();
monstro.mostrarStatus();
disp('----------------------');

