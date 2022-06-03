#!/bin/bash
echo "[-] clean env..."
rm -rf NWPUInfectReport

echo "[-] clone latest version..."
git clone https://hub.xn--gzu630h.xn--kpry57d/F11st/NWPUInfectReport

cp -r NWPUInfectReport/xgdYqtb/* ./

rm -rf NWPUInfectReport

echo "[-] all done..."
