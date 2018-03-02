function [ next_state ] = integrate( state,step_size,function_system,key_name)
%INTEGRATE Summary of this function goes here
%   Detailed explanation goes here
  if(key_name=='RK44') % for now only 1 integrator available
      k1 = function_system(state);
      k2 = function_system(state + step_size*k1/2);
      k3 = function_system(state + step_size*k2/2);
      k4 = function_system(state + step_size*k3);
      next_state = state + (step_size/6)*(k1   + 2*k2   + 2*k3   + k4);
  else
      disp('ERROR invalid integrator');
  end
end

