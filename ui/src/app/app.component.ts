import { Component, ViewChild, ElementRef, AfterViewInit, Input, OnInit, HostListener } from '@angular/core';

declare var ForceGraph3D;
declare var ForceGraphVR;
declare var ForceGraphAR;

import { Vector2 } from 'three';
import { UnrealBloomPass } from '../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AppService } from './app.service.js';
import { Observable } from 'rxjs';
import { of } from 'rxjs/';

@Component({
  selector: 'ngbd-modal-content',
  template: `
    <div class="modal-header">
      <h4 class="modal-title" *ngIf="type == 'node'">Node Data</h4>
      <h4 class="modal-title" *ngIf="type == 'edge'">{{ (edgeResults$ | async)?.title }}</h4>
      <button type="button" class="close" aria-label="Close" (click)="activeModal.dismiss('Cross click')">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div class="modal-body">
      <p *ngIf="type == 'node'">Hello, Node data will be viewed here!</p>
      <p *ngIf="type == 'edge'">
        {{ (edgeResults$ | async)?.sentence }}
      </p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-dark" (click)="activeModal.close('Close click')">Close</button>
    </div>
  `
})
export class NgbdModalContent implements OnInit{
  @Input() type;
  @Input() node;
  @Input() edge;

  edgeResults$: any;

  constructor(
    public activeModal: NgbActiveModal,
    private service: AppService) {}

  ngOnInit(){
    this.edgeResults$ = this.service.edgeApi(this.edge.source.id, this.edge.target.id);
  }
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
  mode = '3D';
  searchResults$: Observable<any> = of({ nodes: [], links: []});
  edgeResults$: Observable<any[]>;

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
    // this.service.fetchGraph(0);
  }

  ngAfterViewInit(){
    // this.postProcessing();
  }

  initializeGraph() {
    // switch(this.mode){
    //   case '3D':
    //     this.Graph = ForceGraph3D();
    //   case 'VR':
    //     this.Graph = ForceGraphVR();
    //   case 'AR':
    //     console.log('AR mode')
    //     this.Graph = ForceGraphAR();
    //   default:
    //     this.Graph = ForceGraph3D();
    // }
    this.Graph = ForceGraph3D();
    this.Graph(this.graph.nativeElement)
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


  // emitParticles(){
  //   [...Array(10).keys()].forEach(() => {
  //     const link = this.gData.links[Math.floor(Math.random() * this.gData.links.length)];
  //     this.Graph.emitParticle(link);      
  //   });
  //   const modalRef = this.modalService.open(NgbdModalContent);
  //   modalRef.componentInstance.type = 'node';
  // }

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
      this.service.searchApi(this.searchForm.get('term').value).subscribe(x => {
        this.gData = x;
        this.initializeGraph();
      }, (err) => {
        console.log('search error');
        console.log(err);
      });
    }
  }

}
