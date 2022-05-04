#!/bin/bash
echo "[-] clean env..."
rm -rf src/ NWPUInfectReport/

echo "[-] clone latest version..."
git clone https://hub.xn--gzu630h.xn--kpry57d/F11st/NWPUInfectReport

mkdir src
cp -r NWPUInfectReport/xgdYqtb/* src/

echo "[-] all done..."
