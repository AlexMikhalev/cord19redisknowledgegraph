import { Component, ViewChild, ElementRef, AfterViewInit, Input, OnInit, HostListener } from '@angular/core';

declare var ForceGraph3D;
import { Vector2 } from 'three';
import { UnrealBloomPass } from '../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AppService } from './app.service.js';
import { ifStmt } from '@angular/compiler/src/output/output_ast';

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
export class AppComponent implements AfterViewInit, OnInit {
  
  @ViewChild('graph', { static: true }) graph: ElementRef;
  Graph: any;
  gData: any;
  searchForm: FormGroup;
  canvasHeight: number;

  constructor(
    private modalService: NgbModal, 
    fb: FormBuilder,
    private service: AppService){
    this.searchForm = fb.group({
      'term': ['', Validators.required]
    });
  }

  ngOnInit(){
    this.canvasHeight = window.innerHeight - 50;
    this.service.fetchGraph(0);
  }

  ngAfterViewInit(){
    this.initializeGraph(this.graph.nativeElement);
    this.postProcessing();
  }

  initializeGraph(htmlElement) {
    // Random tree

    this.service.graphData$.subscribe(graph => {
      this.gData = {
        nodes: graph.data.map(i => ({ id: i[0], name: i[1] }))
      }
    })
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

    // container layout
    this.Graph.height(this.canvasHeight)
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.canvasHeight = window.innerHeight - 50;
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
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.type = 'node';
    modalRef.componentInstance.node = node;
  }

  onLinkClick(node, event){
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.type = 'edge';
    modalRef.componentInstance.edge = node;
  }

  postProcessing(){
    const strength = 0.7;
    const radius = 0.2;
    const threshold = 0;
    const bloomPass = new UnrealBloomPass(new Vector2(128, 128), strength, radius, threshold);
    this.Graph.postProcessingComposer().addPass(bloomPass);
  }


  search(){
    if(this.searchForm.valid){
      this.service.search(this.searchForm.get('term').value);
    }
  }

}
