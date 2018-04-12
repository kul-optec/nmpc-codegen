% radius = 1;
% radius2 = radius*(1/3);
% radius3 = radius*(2/3);
% radius4 = radius*(1/2);
% 
% center = [0;0];

% A = [
% 1     center(1)          center(1)^2            center(2)      center(2)^2 ;
% 1  center(1)+radius  (center(1)+radius)^2  center(2)+radius (center(2)+radius)^2 ;
% 1  center(1)-radius  (center(1)-radius)^2  center(2)+radius (center(2)+radius)^2 ;
% 1  center(1)+radius  (center(1)+radius)^2  center(2)-radius (center(2)-radius)^2 ;
% 1  center(1)-radius  (center(1)-radius)^2  center(2)-radius (center(2)-radius)^2 ;
% 1  center(1)+radius2  (center(1)+radius2)^2  center(2)+radius2 (center(2)+radius2)^2 ;
% 1  center(1)-radius2  (center(1)-radius2)^2  center(2)+radius2 (center(2)+radius2)^2 ;
% 1  center(1)+radius2  (center(1)+radius2)^2  center(2)-radius2 (center(2)-radius2)^2 ;
% 1  center(1)-radius2  (center(1)-radius2)^2  center(2)-radius2 (center(2)-radius2)^2 ;
% 1  center(1)+radius3  (center(1)+radius3)^2  center(2)+radius3 (center(2)+radius3)^2 ;
% 1  center(1)-radius3  (center(1)-radius3)^2  center(2)+radius3 (center(2)+radius3)^2 ;
% 1  center(1)+radius3  (center(1)+radius3)^2  center(2)-radius3 (center(2)-radius3)^2 ;
% 1  center(1)-radius3  (center(1)-radius3)^2  center(2)-radius3 (center(2)-radius3)^2 ;
% 1  center(1)+radius4  (center(1)+radius4)^2  center(2)+radius4 (center(2)+radius4)^2 ;
% 1  center(1)-radius4  (center(1)-radius4)^2  center(2)+radius4 (center(2)+radius4)^2 ;
% 1  center(1)+radius4  (center(1)+radius4)^2  center(2)-radius4 (center(2)-radius4)^2 ;
% 1  center(1)-radius4  (center(1)-radius4)^2  center(2)-radius4 (center(2)-radius4)^2 ;
%     ];
% % 
% b = [1; 0; 0; 0; 0;1/8;1/8;1/8;1/8;3/8;3/8;3/8;3/8;7/10;7/10;7/10;7/10;];
% % 
% x = A\b;

% Lag = @(x) ((x-))
% a=1;
% 
% f(x) a*x^2+b*x+ c;