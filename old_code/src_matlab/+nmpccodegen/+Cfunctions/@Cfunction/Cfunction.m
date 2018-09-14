classdef Cfunction
    %CFUNCTION Interface of a function that can be generated as C code.
    %   This interface is usually used on a function that is the proximal 
    %   of a ProximalFunction. More information on this in the class 
    %   ProximalFunction.    
    methods(Abstract)
        generate_c_code(obj,location);
    end
end

