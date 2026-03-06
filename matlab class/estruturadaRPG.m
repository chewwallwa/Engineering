clear; clc;

% Criando personagens como estruturas
heroi.Nome = 'Thierry';
heroi.Vida = 30;
heroi.Ataque = 45;
heroi.Defesa = 5;

monstro.Nome = 'Monstro';
monstro.Vida = 100;
monstro.Ataque = 16;
monstro.Defesa = 7;

% Mostrando status inicial
disp('--- STATUS INICIAL ---');
mostrarStatus(heroi);
mostrarStatus(monstro);
disp('----------------------');

% Simulando batalha
[heroi, monstro] = luta(heroi, monstro);

% Resultado final
if heroi.Vida > 0
    fprintf('%s venceu!\n', heroi.Nome);
else
    fprintf('%s venceu!\n', monstro.Nome);
end

% Mostrando status final
disp('--- STATUS FINAL ---');
mostrarStatus(heroi);
mostrarStatus(monstro);
disp('----------------------');

%% --- Funções ---

function [p1, p2] = luta(p1, p2)
    while p1.Vida > 0 && p2.Vida > 0
        [p1, p2] = atacar(p1, p2);

        if p2.Vida > 0
            [p2, p1] = atacar(p2, p1);
        end

        pause(1);
    end
end

function [atacante, alvo] = atacar(atacante, alvo)
    dado = randi(6);
    dano = round(atacante.Ataque * (1 - (dado / 10)), 0);
    dano = max(1, dano - alvo.Defesa); % Dano mínimo de 1
    alvo.Vida = max(0, alvo.Vida - dano);

    fprintf('%s atacou %s causando %d de dano! (%d de vida restante)\n', ...
        atacante.Nome, alvo.Nome, dano, alvo.Vida);
end

function mostrarStatus(personagem)
    fprintf('Nome: %s | Vida: %d | Ataque: %d | Defesa: %d\n', ...
        personagem.Nome, personagem.Vida, personagem.Ataque, personagem.Defesa);
end
