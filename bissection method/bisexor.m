clear, clc,close all, tic()

% =========================================================================
% programa que calcula intervalos com raízes pelo teorema de Bolzano, e
% encontra as raízes de cada intervalo pelo método da bissecção.
% 
% https://www.geogebra.org/calculator/h94baspj : a visual explanation of
% the method
% 
% both made by masthierryi - lamec-ufpi.com
% =========================================================================

nroot = 10; % numerode raízes encontradas
% ajuste o intervalo vertical do plot manualmente

%% ============================== FUNÇÕES =================================

% COMUNS ------------------------------------------------------------------

% y =  abs(x);              
% y =  @(x)x.^2 - 1;
% y =  @(x)x;                   
% y =  @(x)4*x + 1;
% y =  @(x)x.^2 - 3*x + 2;       
% y =  @(x)log10(x);            
% y =  @(x)x.*log(x);            
% y =  @(x)sin(x);
y =  @(x)cos(x);
% y =  @(x)2.^x - 3;

% TRANSCEDENTAIS ----------------------------------------------------------

% y =  @(x)cos(x).*cosh(x)-1; 
% y = @(x)(x.^2).* cosh(x.^2)- (x.^2).*sinh(x.^2) - 2*(x.^2).*cosh(x).*cos(x) + x.^2;
% y =  @(x)1-2*cos(x).*cosh(x)+(cosh(x)).^2 -(sinh(x)).^2;

% PROBLEMÁTICAS -----------------------------------------------------------

% y =  @(x)tan(x);
% y =  @(x)sin(x) - 1;          % a função é sempre negativa
% y =  @(x)sin(x.*100);          % precisa de um passo pequeno
% y =  @(x)tan(pi - x)-x;       % descontínua

% IMPOSSIVEIS? ------------------------------------------------------------

% y =  @(x)2.^x;                 %sem raizes

% -------------------------------------------------------------------------

%% ========================= MÉTODO DE BOLZANO ============================

e = 0.0005;            % Precisão do método (distância entre a e b)
xmax = 10^3;           % Intervalo máximo no eixo x onde serão procurados intervalos com raiz

a = 0;                 % Definição do intervalo inicial [a, b]
b = a + e;             % b começa logo após a com o passo e
aux = 0;               % Variável auxiliar para contar os intervalos encontrados
intervalos = zeros(nroot, 4); % Matriz para armazenar os intervalos onde há mudança de sinal

% Loop para encontrar os intervalos onde há mudança de sinal (indício de raiz)
while a <= xmax && aux < nroot  % Garante que o laço não rode infinitamente
    
    if y(a) * y(b) <= 0  % Se houver mudança de sinal entre f(a) e f(b), há uma raiz no intervalo
        aux = aux + 1;  % Incrementa o contador de intervalos encontrados
        
        % Armazena o intervalo encontrado e os valores de f(a) e f(b)
        intervalos(aux, 1) = a;
        intervalos(aux, 2) = b;
        intervalos(aux, 3) = y(a);
        intervalos(aux, 4) = y(b);
        
        % Avança para o próximo intervalo
        a = b;
        b = a + e;
    else
        % Se não houver mudança de sinal, apenas avança para o próximo intervalo
        a = b;
        b = a + e;
    end
end

%% ========================= MÉTODO DA BISSECÇÃO ==========================

erro = 1e-6;          % Precisão desejada para encontrar a raiz
xerr = abs((b - a) / 2);  % Erro inicial
inte = 0;            % Contador de iterações para a bissecção

u = 1;               % Índice para percorrer os intervalos encontrados
i = 1;               % Índice para armazenar as raízes encontradas
raizes = zeros(1, nroot);  % Vetor para armazenar as raízes

% Loop para aplicar o método da bisseção em cada intervalo encontrado
while u <= nroot
    a = intervalos(u, 1);  % Define o início do intervalo
    b = intervalos(u, 2);  % Define o fim do intervalo

    while xerr > erro && inte <= 1.0e4  % Critério de parada: erro menor que o desejado ou limite de iterações atingido
        inte = inte + 1;  % Incrementa o número de iterações
        
        r = (a + b) / 2;  % Calcula o ponto médio (nova aproximação da raiz)
        
        if y(a) * y(r) <= 0  % Se houver mudança de sinal entre f(a) e f(r), a raiz está entre a e r
            b = r;  % Atualiza o fim do intervalo
        else
            a = r;  % Atualiza o início do intervalo
        end
        
        raizes(1, i) = r;  % Armazena a raiz aproximada
    end

    i = i + 1;  % Passa para a próxima raiz
    u = u + 1;  % Passa para o próximo intervalo
    inte = 0;   % Reseta o número de iterações para o próximo intervalo
end

%% ============================ RESULTADOS ================================

% Exibe as raízes encontradas
disp(func2str(y));
disp(raizes(1, 1:aux));

% Verifica se há menos raízes do que o número máximo esperado (nint)
if nroot > aux
    fprintf('A função tem %d raiz(es) real(is) positiva(s)\n\n', aux);
end

% Gera pontos para o gráfico da função
xplot = linspace(min(min(intervalos(:,1:2))), max(max(intervalos(:,1:2))), 10^3);
yplot = y(xplot);

% Plota a função e as raízes encontradas
figure
hold on
plot(xplot, yplot);  % Gráfico da função
ylim([-100, 100])    % Define os limites do eixo Y para evitar distorções
scatter(raizes, zeros(1, size(raizes, 2)));  % Plota as raízes como pontos no eixo X

% =========================================================================
toc()

