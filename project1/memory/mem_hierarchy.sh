
echo "getting memory info..."

hwloc-ls --whole-system --no-io -f --of fig mem_hierarchy.fig
hwloc-ls --whole-system --no-io -f --of txt mem_hierarchy.txt
lscpu > mem_hierarchy_cpuinfo.txt

echo "all done."