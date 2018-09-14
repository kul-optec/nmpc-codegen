classdef ProximalFunction < nmpccodegen.Cfunctions.Cfunction
    %PROXIMALFUNCTION A function of which the proximal operator is
    %defined.
    %   When creating controller object, and input constraint must be
    %   provided this this input constraint must be off the Proximal 
    %   function type. Nmpccodegen Provides a few example functions,
    %   however it is possible to create your own constraint functions.
    %   This interface must be used on your own defined functions.
    
    properties
        prox
    end    
end

