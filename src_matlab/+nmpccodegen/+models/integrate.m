function [ next_state ] = integrate( state,step_size,function_system,key_name)
%INTEGRATE Summary of this function goes here
%   Detailed explanation goes here
next_state = integrate_lib(state,step_size,function_system,key_name);

%   if(key_name=='RK44') % for now only 1 integrator available
%       k1 = function_system(state);
%       k2 = function_system(state + step_size*k1/2);
%       k3 = function_system(state + step_size*k2/2);
%       k4 = function_system(state + step_size*k3);
%       next_state = state + (step_size/6)*(k1   + 2*k2   + 2*k3   + k4);
%   else
%       disp('ERROR invalid integrator');
%   end
end

function [ x_new ] =integrate_lib(x,step_size,function_system,key_name)
%INTEGRATE Integrate using an explicit integration tableau from ./integrator_tableaus
%   x : current state
%   step_size : discretizator step size
%   function_system : continious differential equation of the system
%   behavior
%   key_name : name of the integrator
%         BS5         Bogacki-Shampine RK5(4)8    
%         BuRK65      Butcher's RK65              
%         CMR6        Calvo 6(5)                  
%         DP5         Dormand-Prince RK5(4)7      
%         FE          Forward Euler               
%         Fehlberg45  Fehlberg RK5(4)6            
%         Heun33      Heun RK 33                  
%         Lambert65   Lambert                     
%         MTE22       Minimal Truncation Error 22 
%         Merson43    Merson RK4(3)               
%         Mid22       Midpoint Runge-Kutta        
%         NSSP32      non-SSPRK 32                
%         NSSP33      non-SSPRK 33                
%         PD8         Prince-Dormand 8(7)         
%         RK44        Classical RK4               
%         SSP104      SSPRK(10,4)                 
%         SSP22       SSPRK 22                    
%         SSP22star   SSPRK22star                 
%         SSP33       SSPRK 33                    
%         SSP53       SSP 53                      
%         SSP54       SSP 54                      
%         SSP63       SSP 63                      
%         SSP75       SSP 75                      
%         SSP85       SSP 85                      
%         SSP95       SSP 95  
    models_folder = fileparts(which('nmpccodegen.models.integrate'));
    integrator_folder = strcat(models_folder,'/integrator_tableaus/');
    load(strcat(integrator_folder,key_name,'.mat'));
    
    number_of_states = length(x);
    [number_of_samples,~]=size(A);
    
    % phase 1: calculate the k's
    % k1 = f(x_n)
    % k2 = f(x_n + h(a_21 k_1))
    % k3 = f(x_n + h(a_31 k_1 + a32 k2))
    % ...
    
    k=casadi.SX.sym('k',number_of_states,number_of_samples);
    k(:,1) = function_system(x);
    
    for i=2:number_of_samples
        x_step=zeros(number_of_states,1);
        for j=1:i-1
            x_step = x_step + A(i,j)*k(:,j);
        end
        x_step_scaled = x_step*step_size;
        x_local = x + x_step_scaled ;
       
        k(:,i) = function_system(x_local);
    end
    
    % phase 2: use k's to calculate next state
    % x_{n+1} = x_n + h \sum_{i=1}^s b_i \cdot k_i
    x_new=zeros(number_of_states,1);
    for i=1:number_of_samples
        x_new = x_new + k(:,i)*b(i);
    end
    x_new = x_new*step_size;
    x_new = x_new + x;
end
