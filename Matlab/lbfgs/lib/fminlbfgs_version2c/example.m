% options = struct('GradObj','on','Display','iter','LargeScale','off','HessUpdate','bfgs','InitialHessType','identity','GoalsExactAchieve',0);
a=1;
b=100;
theoretical_solution=[a;a^2];
options = struct('GradObj','on','Display','iter','LargeScale','off','HessUpdate','lbfgs','InitialHessType','identity','GoalsExactAchieve',1,'GradConstr',false,'StoreN',20);

x0 =[-1.2;1.];
tic
[x2,fval2] = fminlbfgs(@myfun,x0,options);
toc

x0 =[0.5;0.5];
tic
[x2,fval2] = fminlbfgs(@myfun_poly,x0,options);
toc


% tic
% [x,fval] = fminunc(@myfun,x0,options);
% toc
