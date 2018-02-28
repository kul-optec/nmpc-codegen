function [ fxu ] = trailer_dyn(L,x,u)
    theta_dot = ( -u(1) * sin(x(3)) + u(2) * cos(x(3)) ) / L;
    fxu = [ ( u(1) + L * sin(x(3) ) * theta_dot);
            ( u(2) - L * cos(x(3) ) * theta_dot);
            theta_dot ];
end