
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';
import {Component} from '@angular/core';

export interface Vegetable {
  name: string;
}

/**
 * @title Chips Drag and Drop
 */
 @Component({
  selector: 'app-chips-dnd',
  templateUrl: './chips-dnd.component.html',
  styleUrls: ['./chips-dnd.component.css']
})
export class ChipsDndComponent {
  vegetables: Vegetable[] = [
    {name: 'apple'},
    {name: 'banana'},
    {name: 'strawberry'},
    {name: 'orange'},
    {name: 'kiwi'},
    {name: 'cherry'},
  ];

  drop(event: CdkDragDrop<Vegetable[]>) {
    moveItemInArray(this.vegetables, event.previousIndex, event.currentIndex);
  }
}
