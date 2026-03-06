function [y] = funcao(x) % FUNÇÕES

    % COMUNS --------------------------------------------------------------
    
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
    
    % TRANSCEDENTAIS ------------------------------------------------------
    
    % y =  @(x)cos(x).*cosh(x)-1; 
    % y = @(x)(x.^2).* cosh(x.^2)- (x.^2).*sinh(x.^2) - 2*(x.^2).*cosh(x).*cos(x) + x.^2;
    % y =  @(x)1-2*cos(x).*cosh(x)+(cosh(x)).^2 -(sinh(x)).^2;
    
    % PROBLEMÁTICAS -------------------------------------------------------
    
    % y =  @(x)tan(x);
    % y =  @(x)sin(x) - 1;          % a função é sempre negativa
    % y =  @(x)sin(x.*100);          % precisa de um passo pequeno
    % y =  @(x)tan(pi - x)-x;       % descontínua
    
    % IMPOSSIVEIS? --------------------------------------------------------
    
    % y =  @(x)2.^x;                 %sem raizes
    
    % ---------------------------------------------------------------------

end
