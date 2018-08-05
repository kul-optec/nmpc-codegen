function trailer_printer( state_history,amplitude,color )
%TRAILER_PRINTER Prints state history of trailer
%   Detailed explanation goes here
    
        u = cos(state_history(3,:))*amplitude;
        v = sin(state_history(3,:))*amplitude;
    for i=1:size(state_history,2)
        quiver(state_history(1,i),state_history(2,i),u(i),v(i),'color',color,'MaxHeadSize',0.5);
    end

end

