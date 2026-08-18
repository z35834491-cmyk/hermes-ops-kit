#!/usr/bin/env python3
"""Hermes Ops Kit onboarding skeleton.

v0.1 只定义接口，不做危险操作。
"""
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="env-map yaml path")
    p.add_argument("--env", help="environment name")
    args = p.parse_args()
    print("onboard.py skeleton: next step is implementing safe read-only discovery")
    print(f"config={args.config} env={args.env or 'all'}")


if __name__ == "__main__":
    main()
