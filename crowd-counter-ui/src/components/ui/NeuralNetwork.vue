<template>
    <div class="neural-network" ref="networkContainer">
      <svg ref="networkSvg" class="network-svg"></svg>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import * as d3 from 'd3';
  
  // Props for network configuration
  const props = defineProps({
    nodes: {
      type: Array as () => { id: string; value: number; group: number }[],
      default: () => []
    },
    links: {
      type: Array as () => { source: string; target: string; value: number }[],
      default: () => []
    }
  });
  
  // Refs for container and SVG
  const networkContainer = ref<HTMLElement | null>(null);
  const networkSvg = ref<SVGElement | null>(null);
  
  // D3 simulation
  let simulation: any = null;
  
  // Initialize the neural network
  const initNetwork = () => {
    if (!networkContainer.value || !networkSvg.value) return;
    
    // Clear any existing elements
    d3.select(networkSvg.value).selectAll('*').remove();
    
    // Set width and height
    const width = networkContainer.value.clientWidth;
    const height = networkContainer.value.clientHeight;
    
    // Update SVG dimensions
    d3.select(networkSvg.value)
      .attr('width', width)
      .attr('height', height);
    
    // Create a reusable SVG filter for neuromorphic glow effect
    const defs = d3.select(networkSvg.value).append('defs');
    
    // Neural glow filter
    const filter = defs.append('filter')
      .attr('id', 'neural-glow')
      .attr('width', '300%')
      .attr('height', '300%')
      .attr('x', '-100%')
      .attr('y', '-100%');
      
    filter.append('feGaussianBlur')
      .attr('stdDeviation', '5')
      .attr('result', 'blur');
      
    filter.append('feFlood')
      .attr('flood-color', 'rgba(112, 72, 232, 0.3)')
      .attr('flood-opacity', '1')
      .attr('result', 'color');
      
    filter.append('feComposite')
      .attr('in', 'color')
      .attr('in2', 'blur')
      .attr('operator', 'in')
      .attr('result', 'glow');
      
    filter.append('feMerge')
      .selectAll('feMergeNode')
      .data(['glow', 'SourceGraphic'])
      .enter()
      .append('feMergeNode')
      .attr('in', d => d);
    
    // Synapse filter
    const synapseFilter = defs.append('filter')
      .attr('id', 'synapse-pulse')
      .attr('width', '300%')
      .attr('height', '300%')
      .attr('x', '-100%')
      .attr('y', '-100%');
      
    synapseFilter.append('feGaussianBlur')
      .attr('stdDeviation', '2')
      .attr('result', 'blur');
      
    synapseFilter.append('feColorMatrix')
      .attr('type', 'hueRotate')
      .attr('values', '0')
      .attr('result', 'color')
      .append('animate')
      .attr('attributeName', 'values')
      .attr('values', '0;360;0')
      .attr('dur', '8s')
      .attr('repeatCount', 'indefinite');
      
    synapseFilter.append('feComposite')
      .attr('in', 'color')
      .attr('in2', 'blur')
      .attr('operator', 'in')
      .attr('result', 'pulse');
      
    synapseFilter.append('feMerge')
      .selectAll('feMergeNode')
      .data(['pulse', 'SourceGraphic'])
      .enter()
      .append('feMergeNode')
      .attr('in', d => d);
    
    // Create links (connections between neurons)
    const link = d3.select(networkSvg.value)
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(props.links)
      .enter()
      .append('line')
      .attr('stroke-width', d => Math.sqrt(d.value))
      .attr('stroke', 'rgba(255, 255, 255, 0.2)')
      .attr('stroke-opacity', 0.6)
      .attr('filter', 'url(#synapse-pulse)');
    
    // Create nodes (neurons)
    const node = d3.select(networkSvg.value)
      .append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(props.nodes)
      .enter()
      .append('circle')
      .attr('r', d => Math.max(5, Math.sqrt(d.value) * 3))
      .attr('fill', d => {
        const colors = ['#7048E8', '#00FFFF', '#FF61EF'];
        return colors[d.group % colors.length];
      })
      .attr('filter', 'url(#neural-glow)')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended) as any);
    
    // Add node pulse animation
    node.append('animate')
      .attr('attributeName', 'r')
      .attr('values', d => {
        const baseRadius = Math.max(5, Math.sqrt(d.value) * 3);
        return `${baseRadius};${baseRadius + 2};${baseRadius}`;
      })
      .attr('dur', d => 2 + Math.random() * 3 + 's')
      .attr('repeatCount', 'indefinite');
    
    // Create simulation
    simulation = d3.forceSimulation(props.nodes as any)
      .force('link', d3.forceLink(props.links).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide().radius((d: any) => Math.sqrt(d.value) * 3 + 10));
    
    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);
      
      node
        .attr('cx', (d: any) => d.x = Math.max(10, Math.min(width - 10, d.x)))
        .attr('cy', (d: any) => d.y = Math.max(10, Math.min(height - 10, d.y)));
    });
    
    // Drag functions
    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    
    // Neural activity simulation (pulsing connections)
    setInterval(() => {
      // Randomly activate some connections
      link.each(function(d: any, i: number) {
        if (Math.random() < 0.1) {
          const linkElement = d3.select(this);
          
          linkElement
            .transition()
            .duration(300)
            .attr('stroke', 'rgba(255, 255, 255, 0.8)')
            .attr('stroke-width', d.value * 2)
            .transition()
            .duration(700)
            .attr('stroke', 'rgba(255, 255, 255, 0.2)')
            .attr('stroke-width', Math.sqrt(d.value));
        }
      });
    }, 500);
  };
  
  // Handle window resize
  const handleResize = () => {
    if (simulation) {
      simulation.stop();
    }
    initNetwork();
  };
  
  onMounted(() => {
    // Generate default nodes and links if not provided
    if (props.nodes.length === 0) {
      const defaultNodes = [];
      const defaultLinks = [];
      
      // Create 15 nodes
      for (let i = 0; i < 15; i++) {
        defaultNodes.push({
          id: `node${i}`,
          value: 10 + Math.random() * 40,
          group: Math.floor(Math.random() * 3)
        });
      }
      
      // Create 20 links
      for (let i = 0; i < 20; i++) {
        const source = Math.floor(Math.random() * 15);
        let target = Math.floor(Math.random() * 15);
        while (target === source) {
          target = Math.floor(Math.random() * 15);
        }
        
        defaultLinks.push({
          source: `node${source}`,
          target: `node${target}`,
          value: 1 + Math.random() * 5
        });
      }
      
      props.nodes.push(...defaultNodes);
      props.links.push(...defaultLinks);
    }
    
    // Initialize network
    initNetwork();
    
    // Add resize listener
    window.addEventListener('resize', handleResize);
  });
  
  onBeforeUnmount(() => {
    // Clean up
    window.removeEventListener('resize', handleResize);
    
    if (simulation) {
      simulation.stop();
    }
  });
  </script>
  
  <style>
  .neural-network {
    width: 100%;
    height: 400px;
    position: relative;
    overflow: hidden;
    border-radius: var(--radius-lg);
    background-color: rgba(18, 26, 41, 0.8);
  }
  
  .network-svg {
    width: 100%;
    height: 100%;
  }
  </style>
  