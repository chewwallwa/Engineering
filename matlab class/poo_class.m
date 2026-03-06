classdef poo_class_file2
    properties
        i = 20:30
        j = 1:10
        k = 10:20

        result
    end

    methods
        function obj = poo_class_file2() % construtor
            obj = mean(obj);
        end

        function obj = mean(obj)
            obj.result.for_i = mean(obj.i); 
        end
    end
end