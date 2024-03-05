{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    python311Packages.torch
    python311Packages.nvidia-ml-py
    stdenv.cc.cc.lib
    zlib
  ]);
  runScript = "bash";
}).env

# see: https://nixos.wiki/wiki/Python
# for direction on how to enter and use the environment in nixos
# tldr:
# nix-shell pip-shell.nix
# virtualenv venv
# source venv/bin/activate
# pip install -r requirements.txt
# try
# TMPDIR=/home/josiah/tmp/ pip install -r requirements.txt
# For big packages where /tmp runs out of space
# TMPDIR=/home/josiah/tmp/ python3 -m pip install ultralytics