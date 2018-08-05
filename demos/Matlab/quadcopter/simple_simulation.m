% get example model from lib
[system_equations, number_of_states, number_of_inputs, coordinates_indices] ...
    = nmpccodegen.example_models.get_quadcopter_model();

step_size=0.05;
integrator = 'RK44';  % select a Runga-Kutta  integrator (FE is forward euler)

constraint_input = nmpccodegen.Cfunctions.IndicatorBoxFunction([0, 0, 0, 0], [100, 100, 100, 100]);  % input needs stay within these borders

model = nmpccodegen.models.Model_continuous(system_equations, constraint_input, step_size, number_of_states, ...
                                number_of_inputs, coordinates_indices, integrator);

% set starting point
init_state = zeros(12,1);init_state(1)=3;init_state(2)=3;init_state(3)=3;

% simulate
number_of_steps=100;
state = init_state;
input=zeros(4,1)*10; % fly straight up
state_history=zeros(12,number_of_steps);
for i=1:100
    state = model.get_next_state_double(state,input);
    state_history(:,i)=state;
    
end
%%
figure;
range=1:10;
plot3(state_history(1,range),state_history(2,range),state_history(3,range))