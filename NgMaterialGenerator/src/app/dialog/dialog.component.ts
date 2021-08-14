import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent implements OnInit {
  @Input() type?: number;
  data: any;
  animal: string;
  name: string;

  constructor() { 
    this.name = '1111';
    this.animal = '22222222';
    this.data = {name: this.name, animal: this.animal};
  }

  ngOnInit(): void {
  }

}
