
%Parameters
roh = 1.225;
Cw = 0.31;
A = 2.05;
tire_r = 0.33;
tire_c = 3.14 * tire_r * 2;
m = 1580;
gearshift_delay = 0;
gear = 1;

rpm_axis = [0 1000 2000 3000 4000 5000 6000 7000 7200];
Tq = 0.8 * [400 400 400 500 600 600 550 400 0];



t_vect = (0.1:0.1:35);
v_vect = zeros(1,350);
v_vect(1) = 50 / 3.6;
rpm_vect = zeros(1,350);

count = 0;
gears = [3.59 2.19 1.41 1 0.83];
final_gear = 3.36;


for t = (1:1:350)
    if (count > 0) && (count<gearshift_delay)
        count = count + 1
    else
        
        count = 0;    
        Fair = roh * v_vect(t)^2 * Cw * A / 2;
        rpm = 60 * gears(gear) * final_gear * v_vect(t)/ tire_c;
        rpm_vect(t) = rpm;
        Ftq = interp1(rpm_axis,Tq,rpm) * gears(gear) * final_gear / tire_r;
        a = (Ftq - Fair) / m;
    
        v_vect(t+1) = v_vect(t) + a * 0.1; 
        
        if rpm > 6800
            gear = min(gear + 1,5);
            count = count + 1;
        end
    end
   
end

v_vect = v_vect .* 3.6;
plot(t_vect,v_vect(1:350))
figure;
plot(t_vect,rpm_vect,'r')
