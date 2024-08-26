clc
clear

% Load input data
Nodes= load('Nodes2.txt');
Links= load('Links2.txt');
L= load('L2.txt');

nNodes= size(Nodes,1);
nLinks= size(Links,1);
G=graph(L);

% Set parameters
Cmax = 1000;      
n = 10;             % Size of solutions  
r = 3;              % Randomization factor for greedy
time = 30;          % Time limit in seconds

% Array to store all best solutions
solution_values = [];

for i = 1:10
    % Execute GRASP algorithm
    [best_solution, best_val] = GRASP(G,n,Cmax,r,time,nNodes)

    % Store best value in each iteration
    solution_values = [solution_values best_val];
end

% Display all best solutions found and statistics
solution_values
max_val = max(solution_values)
min_val = min(solution_values)
avg_val = mean(solution_values)



% GRASP algorithm implementation 
function [best_solution, best_val] = GRASP(G,n,Cmax,r,time,nNodes)
    best_solution = greedy_random(G,n,nNodes,Cmax, r);
    [best_solution, best_val] = sahc(G,n,nNodes,Cmax,best_solution);

    tic;
    while (toc < time)
        solution = greedy_random(G,n,nNodes,Cmax, r);
        [solution, val] = sahc(G,n,nNodes,Cmax,solution);
        if val < best_val
            best_solution = solution;
            best_val = val;
        end
    end
end

% Steepest Ascent Hill Climbing implementation
function [s, best_val] = sahc(G,n,nNodes,Cmax,s)
    improved = true;
    [best_val, max] = AverageSP_v2(G,s);

    while improved
        temp_s = get_best_neighbour(G,s,nNodes,Cmax);
        [temp_val, temp_max] = AverageSP_v2(G,temp_s);
        if temp_val < best_val
            best_val = temp_val;
            s = temp_s;
        else
            improved = false;
        end
    end
end

% Auxiliary function to get the best neighbor from a set of neighours 
function [bestn] = get_best_neighbour(G,s,nNodes,Cmax)
    bestval = inf;
    bestn = s;
    neighbours = get_neighbours(s,nNodes);
    for i = 1:size(neighbours,1)
        [asp, maxsp] = AverageSP_v2(G,neighbours(1,:));
        if asp < bestval && maxsp <= Cmax
            bestval = asp;
            bestn = neighbours(1,:);
        end
    end
end

% Auxiliary function to find all possible neighbours of a solution
function [Neighbours] = get_neighbours(s,nNodes)
    Neighbours = [];
    Others = setdiff(1:nNodes,s);
    for a= s
        for b= Others
            neigh = [setdiff(s,a) b];
            Neighbours = [Neighbours;neigh];
        end
    end
end

% Implementation of Greedy Randomized
function [s] = greedy_random(G,n,nNodes,Cmax, r)
    s = [];
    E = 1:nNodes;

    for i = 1:n
        R = [];
        for j = E
            [asp, maxsp] = AverageSP_v2(G,[s j]);
            if maxsp <= Cmax
                R = [ R ; j asp ];
            end
        end
        R = sortrows(R,2);
        e = R(randi(r),1);
        s = [s e];
        E = setdiff(E,e);
    end
end