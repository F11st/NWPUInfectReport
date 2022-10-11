#!/bin/bash
echo "[-] clean env..."
rm -rf NWPUInfectReport

echo "[-] clone latest version..."
git clone https://ghproxy.com/https://github.com/F11st/NWPUInfectReport

cp -r NWPUInfectReport/xgdYqtb/* ./

rm -rf NWPUInfectReport

echo "[-] all done..."
