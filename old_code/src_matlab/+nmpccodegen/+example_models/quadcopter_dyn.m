function [ dstate ] = quadcopter_dyn( params, state , input )
    %QUADCOPTER_DYN Returns dx = f(x) for the quadcopter
    %   State
    %     x = [x y z vx vy vz phi theta gamma omega_x omega_y omega_z];
    %   Input: (voltages on each motor)
    %     u = [u_1 u_2 u_3 u_4]
    %   The following parameters should be provided
    %     params.mass_quadcopter;
    %     params.radius_quadcopter;
    %     params.propeller_lift_coefficient;
    %     params.propeller_drag_coefficient;
    %     params.gravity_acceleration;
    %     params.air_friction_coefficient;
    %     params.quadcopter_initeria_x_axis;
    %     params.quadcopter_initeria_y_axis;
    %     params.quadcopter_initeria_z_axis;
    %     params.motor_constant;
    m = params.mass_quadcopter;
    L = params.radius_quadcopter;
    k = params.propeller_lift_coefficient;
    b = params.propeller_drag_coefficient;
    g = params.gravity_acceleration;
    kd = params.air_friction_coefficient;
    Ixx = params.quadcopter_initeria_x_axis;
    Iyy = params.quadcopter_initeria_y_axis;
    Izz = params.quadcopter_initeria_z_axis;
    cm = params.motor_constant;
    
    % read out the current state
    x=state(1);vx = state(4);phi=state(7);omega_x=state(10);
    y=state(2);vy = state(5);theta=state(8);omega_y=state(11);
    z=state(3);vz = state(6);gamma=state(9);omega_z=state(12);
    
    dstate=casadi.SX.sym('dstate',12,1);

    dstate(1) = vx;
    dstate(2) = vy;
    dstate(3) = vz;
    
    dstate(4) = - (kd/m)*vx + ((k*cm)/m)*(sin(gamma)*sin(phi)+cos(gamma)*cos(phi)*sin(theta))*sum(input);
    dstate(5) = - (kd/m)*vy + ((k*cm)/m)*(cos(phi)*sin(gamma)*sin(theta)-cos(gamma)*sin(phi))*sum(input);
    dstate(6) = - (kd/m)*vz -g + ((k*cm)/m)*(cos(theta)*cos(phi))*sum(input);
    
    dstate(7) = omega_x + omega_y*(sin(phi)*tan(theta)) + omega_z*(cos(phi)*tan(theta));
    dstate(8) = omega_y*cos(phi) - omega_z*sin(phi);
    dstate(9) = omega_y*(sin(phi)/cos(theta)) + omega_z*(cos(phi)/cos(theta));
    
    dstate(10) = ((L*k*cm)/(Ixx))*(input(1)-input(3)) - ((Iyy-Izz)/(Ixx))*omega_y*omega_z;
    dstate(11) = ((L*k*cm)/(Iyy))*(input(2)-input(4)) - ((Izz-Ixx)/(Iyy))*omega_x*omega_z;
    dstate(12) = ((b*cm)/(Izz))*(input(1) - input(2) + input(3) - input(4)) - ((Ixx-Iyy)/(Izz))*omega_x*omega_y;
end

