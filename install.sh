#!/bin/bash
echo "[-] clean env..."
rm -rf src/ NWPUInfectReport/

echo "[-] clone latest version..."
git clone https://github.com/F11st/NWPUInfectReport

mkdir src
cp -r NWPUInfectReport/xgdYqtb/* src/
echo "[-] all done..."
