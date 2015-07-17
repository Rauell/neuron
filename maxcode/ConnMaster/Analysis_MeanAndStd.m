function [results] = Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s, a)

results = zeros(20,8);
results(:,1) = mean(SPIKE)';
results(:,3) = mean(SPIKE_GRID(:,:,1))';
results(:,5) = mean(SPIKE_GRID(:,:,2))';
results(:,7) = mean(SPIKE_GRID(:,:,3))';

results(:,2) = std(SPIKE)';
results(:,4) = std(SPIKE_GRID(:,:,1))';
results(:,6) = std(SPIKE_GRID(:,:,2))';
results(:,8) = std(SPIKE_GRID(:,:,3))';

hold on
x = linspace(5,100,20)';
if a == 1,
    if s == 1,
        errorbar(x,results(:,1), results(:,2), 'LineWidth',2, 'Color', 'k')

    elseif s == 2,
        errorbar(x,results(:,3), results(:,4), 'LineWidth',2, 'Color', 'k')

    elseif s == 3,

        errorbar(x,results(:,5), results(:,6), 'LineWidth',2, 'Color', 'k')
    else

        errorbar(x,results(:,7), results(:,8), 'LineWidth',2, 'Color', 'k')
    end
else
    if s == 1,
        errorbar(x,results(:,1), results(:,2), 'LineWidth',2, 'Color', 'r')

    elseif s == 2,
        errorbar(x,results(:,3), results(:,4), 'LineWidth',2, 'Color', 'r')

    elseif s == 3,

        errorbar(x,results(:,5), results(:,6), 'LineWidth',2, 'Color', 'r')
    else

        errorbar(x,results(:,7), results(:,8), 'LineWidth',2, 'Color', 'r')
    end
end