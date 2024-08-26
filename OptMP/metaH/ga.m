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
time = 30;          % Time limit in seconds
Psize = 10;         % Population size
q = 0.2;            % Probability of mutation


% Array to store all best solutions
solution_values = [];

for i = 1:10
    % Execute GA algorithm
    [best_solution, best_val] = GA(G,n,Cmax,Psize,time,nNodes,q)
    % Store best value in each iteration
    solution_values = [solution_values best_val];
end

% Display all best solutions found and statistics
solution_values
max_val = max(solution_values)
min_val = min(solution_values)
avg_val = mean(solution_values)


% Genetic Algorithm
function [best_solution, best_val] = GA(G,n,Cmax,Psize,time,nNodes,q)
    % Generate initial population
    population = [];
    for i = 1:Psize
        population = [population ; generate_valid_solution(n,nNodes, G, Cmax)];
    end
    
    tic;
    while (toc < time)
        new_pop = [];
    
        % Generate new population through selection, crossover, and mutation
        for i = 1:Psize
            while true
                s = crossover(G,population,Psize,n);
                if is_valid(s,G,Cmax)
                    break
                end
            end
    
            randomNumber = rand;
            if randomNumber <= q
                s = mutation(s,n,nNodes,G,Cmax);
            end
    
            new_pop = [new_pop ; s];
        end
        population = new_pop;
    end

    % Find the best solution and its value in the final population
    best_solution = [];
    best_val = inf;
    
    for i = 1:Psize
        [val, maxsp] = AverageSP_v2(G,population(i,:));
        if val < best_val
            best_solution = population(i,:);
            best_val = val;
        end
    end

end

% Perform mutation on a solution by randomly selecting and changing an element
function [new_s] = mutation(s,n,nNodes,G,Cmax)
    while true
        new_s = s;
        index = randi([1,n],1,1);
        new_s(index) = randi([1,nNodes],1,1);
        if is_valid(new_s,G,Cmax)
            break
        end
    end
end

% Perform crossover by combining two parent solutions
function [s] = crossover(G,P,Psize,n)
    s = [];
    [p1, p2] = parent_selection(G,P,Psize);

    % Generate new individual
    
    for i = 1:n
        randomNumber = rand;
        if randomNumber < 0.5 && ~ismember(p1(i),s)
            s = [s p1(i)];
        else
            s = [s p2(i)];
        end
    end
end

% Perform parent selection based on the fitness probabilities
function [p1, p2] = parent_selection(G,P,Psize)
    probabilities = [];
    p1 = -1;
    p2 = -1;

    for i = 1:Psize
        [asp, maxsp] = AverageSP_v2(G,P(i));
        probabilities = [probabilities ; i 1/asp];
    end

    probabilities(:, 2) = probabilities(:, 2) / sum(probabilities(:, 2));
    probabilities = sortrows(probabilities,2);
    
    for i = 2:size(probabilities,1)
        probabilities(i,2) = probabilities(i-1,2)+probabilities(i,2);
    end

    %Get both parents from list
    randomNumber = rand;
    for i = 1:size(probabilities, 1)
        if randomNumber <= probabilities(i, 2)
            p1 = probabilities(i, 1);
            break;
        end
    end

    randomNumber = rand;
    for i = 1:size(probabilities, 1)
        if randomNumber <= probabilities(i, 2) && probabilities(i, 1) ~= p1
            p2 = probabilities(i, 1);
            break;
        end
    end

    if p2 == -1
        p2 = probabilities(1, 1);
    end

    % Get individuals with id
    p1 = P(p1,:);
    p2 = P(p2,:);

end

% Generate a valid solution by random permutation until a valid one is found
function [s] = generate_valid_solution(n, nNodes, G, Cmax)
    not_valid = true;

    while not_valid
        s = randperm(nNodes,n);
        [asp, maxsp] = AverageSP_v2(G,s);
        if maxsp <= Cmax
            not_valid = false;
        end
    end
end

% Check if a solution is valid based on the Cmax constraint and no node repetition
function [validity] = is_valid(s, G, Cmax)
    validity = true;

    [asp, maxsp] = AverageSP_v2(G,s);
    if maxsp > Cmax || asp==-1 || maxsp==-1
        validity = false;
    end
end