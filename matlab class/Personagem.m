classdef Personagem % classe (encapsula prop e metodos)
    properties % propriedades (visibilidade padrão=public)
        Nome
        Vida
        Ataque
        Defesa
    end
    
    methods % metodos
        function obj = Personagem(nome, vida, ataque, defesa) % construtor
            % incicializa um objeto com seus devidos atributos
            obj.Nome = nome;
            obj.Vida = vida;
            obj.Ataque = ataque;
            obj.Defesa = defesa;
        end
        
        function [obj, alvo] = luta(obj,alvo)
            while obj.Vida > 0 && alvo.Vida > 0
                [obj, alvo] = obj.atacar(alvo);

                if alvo.Vida > 0
                    [alvo, obj] = alvo.atacar(obj);
                end

                pause(1);
            end
            % Resultado final
            if obj.Vida > 0
                fprintf('%s venceu!\n', obj.Nome);
            else
                fprintf('%s venceu!\n', alvo.Nome);
            end
        end

        function [obj, alvo] = atacar(obj, alvo) % método
            % encapsulamento: o que acontece aqui, só acontece aqui, e
            % quando terminar só vai ter a entrada, só que atualizada, sem
            % rastros do método.
            %
            % matlab trata objeto como valores, ent o objeto precisa ser
            % atualizado e devolvido pro main file (RPG), por isso o output
            % é a entrada atualizada

            dado = randi(6);
            dano = round(obj.Ataque *(1 - (dado/10)),0);

            dano = max(1, dano - alvo.Defesa);  % Dano mínimo de 1
            alvo.Vida = max(0, alvo.Vida - dano);

            fprintf('%s atacou %s causando %d de dano! (%d de vida restante)\n', ...
                obj.Nome, alvo.Nome, dano, alvo.Vida);
            % mostrarStatus(obj)
        end
        
        function mostrarStatus(obj) % método
            % modularidade: permite usar o mesmo método pra dois objetos
            % diferentes, printa tanto pro monstro quanto pro herói
            fprintf('Nome: %s | Vida: %d | Ataque: %d | Defesa: %d\n', ...
                obj.Nome, obj.Vida, obj.Ataque, obj.Defesa);
        end
    end
end
