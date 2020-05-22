import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

declare var ForceGraph3D;
import { Vector2 } from 'three';
import { UnrealBloomPass } from '../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  @ViewChild('graph', { static: true }) graph: ElementRef;
  Graph: any;
  gData: any;

  ngAfterViewInit(){
    this.initializeGraph(this.graph.nativeElement);
    this.postProcessing();
  }

  initializeGraph(htmlElement) {
    // Random tree
    const N = 50;
    this.gData = {
      nodes: [...Array(N).keys()].map(i => ({ id: i })),
      links: [...Array(N).keys()]
        .filter(id => id)
        .map(id => ({
          source: id,
          target: Math.round(Math.random() * (id - 1))
        }))
    };

    this.Graph = ForceGraph3D()
      (htmlElement)
      .linkDirectionalParticleColor(() => 'red')
      .linkDirectionalParticleWidth(4)
      .linkHoverPrecision(10)
      .graphData(this.gData);

    this.Graph.onLinkClick(this.Graph.emitParticle); // emit particles on link click
  }

  emitParticles(){
    [...Array(10).keys()].forEach(() => {
      const link = this.gData.links[Math.floor(Math.random() * this.gData.links.length)];
      this.Graph.emitParticle(link);
    });
  }

  postProcessing(){
    const bloomPass = new UnrealBloomPass(new Vector2(128, 128), 0.7, 0.2, 0);
    bloomPass.strength = 3;
    bloomPass.radius = 1;
    bloomPass.threshold = 0.1;
    this.Graph.postProcessingComposer().addPass(bloomPass);
  }

}
