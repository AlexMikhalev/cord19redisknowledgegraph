import { Component, ViewChild, ElementRef, AfterViewInit, Input } from '@angular/core';

declare var ForceGraph3D;
import { Vector2 } from 'three';
import { UnrealBloomPass } from '../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'ngbd-modal-content',
  template: `
    <div class="modal-header">
      <h4 class="modal-title" *ngIf="type == 'node'">Node Data</h4>
      <h4 class="modal-title" *ngIf="type == 'edge'">Edge Data</h4>
      <button type="button" class="close" aria-label="Close" (click)="activeModal.dismiss('Cross click')">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <p *ngIf="type == 'node'">Hello, Node data will be viewed here!</p>
      <p *ngIf="type == 'edge'">Hello, Edge data will be viewed here!</p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-dark" (click)="activeModal.close('Close click')">Close</button>
    </div>
  `
})
export class NgbdModalContent {
  @Input() type;
  @Input() node;
  @Input() edges;

  constructor(public activeModal: NgbActiveModal) {}
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  @ViewChild('graph', { static: true }) graph: ElementRef;
  Graph: any;
  gData: any;

  constructor(private modalService: NgbModal){}

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

    // this.Graph.onLinkClick(this.Graph.emitParticle); // emit particles on link click
    this.Graph.onNodeClick(this.onNodeClick.bind(this));
    this.Graph.onLinkClick(this.onLinkClick.bind(this));
  }

  emitParticles(){
    [...Array(10).keys()].forEach(() => {
      const link = this.gData.links[Math.floor(Math.random() * this.gData.links.length)];
      this.Graph.emitParticle(link);
      
    });
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.type = 'node';
  }

  onNodeClick(node, event){
    console.log
    console.log(node)
    console.log(event)
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.type = 'node';
  }

  onLinkClick(node, event){
    console.log(node)
    console.log(event)
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.type = 'edge';
  }

  postProcessing(){
    const bloomPass = new UnrealBloomPass(new Vector2(128, 128), 0.7, 0.2, 0);
    bloomPass.strength = 3;
    bloomPass.radius = 1;
    bloomPass.threshold = 0.1;
    this.Graph.postProcessingComposer().addPass(bloomPass);
  }

}
