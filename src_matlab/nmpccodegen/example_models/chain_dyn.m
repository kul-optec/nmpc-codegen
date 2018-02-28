function [dx, dQ] = chain_dyn(x, u, dim, M, m, D, L, g, bet, gam, del, x_ref)
% CHAIN_DYN: compute the dynamics for the system consisting of M masses,
% attached in a chain, with one end fixed (therefore pos_0 = 0, vel_0 = 0)
% and the other end which is used to control the system
% (therefore u = vel_{M+1}).
%
%   x: state vector (pos_1, ..., pos_M, pos_{M+1}, vel_1, ..., vel_M)
%   u: input vector
%
% Model Parameters:
%
%   dim: dimension of the space
%   M: number of balls composing the chain
%   m: mass of each of the balls
%   D: spring constant
%   L: rest length of the springs
%   g: gravity acceleration
%
% Optimal control problem parameters:
%
%   bet:
%   gam:
%   del:
%   x_ref:
%

% rearrange positions as columns for convenience
X = reshape(x(1:dim*(M+1)), dim, M+1);

% take the sub-vector of velocities
v = x(dim*(M+1)+1:end);

% compute distances between the masses
dist_vect = [X(:, 1), X(:, 2:end)-X(:, 1:end-1)];
dist_norm = sqrt(sum(dist_vect.*dist_vect, 1));

% compute forces
F = dist_vect*diag(D*(1-L./dist_norm));
fs = (F(:, 2:end)-F(:, 1:end-1))/m + repmat(g, 1, M); fs = fs(:);

% compute derivative of the state
dx = [v; u; fs];

if nargout > 1
  % compute derivative of the cost function
  x_end = x(M*dim+1:(M+1)*dim);
  dQ = bet*norm(x_end - x_ref)^2 + gam*norm(v)^2 + del*norm(u)^2;
end
