#include<stdio.h>
#include<assert.h>
#include<stdlib.h>

struct node {
	struct node *next;
	int data;
}*head;

void insertAtTheEnd(int dataToAdd){
	struct node *temp = (struct node*)malloc(sizeof(struct node));
	temp->next = NULL;
	temp->data = dataToAdd;

	if(head == NULL){ /* list is blank */
		head = temp;
		return;
	}
	struct node *curr;
	for(curr = head; curr->next; curr = curr->next);
	curr->next = temp;
}

void insertAtTheBeginning(int dataToAdd){
	struct node *temp = (struct node*)malloc(sizeof(struct node));
	temp->next = head;
	temp->data = dataToAdd;
	head = temp;
}

void printTheList(){
	if(head == NULL)
		return;
	struct node *curr = head;

	for(; curr; curr = curr->next)
		printf("%d->", curr->data);
	printf("NULL\n");

}

void reverse(){
	if(head == NULL || head->next == NULL)
		return;

	struct node *curr = head, *prev = NULL, *nxt = NULL;
	while(curr){
		nxt = curr->next;
		curr->next = prev;
		prev = curr;
		curr = nxt;
	}
	head = prev;
}
/*
void reverseRecursionD(struct node *curr, struct node *prev, struct node **head){
	if(!curr->next){
		*head = curr;
		curr->next = prev;
	}
	struct node *nxt = curr->next;
	curr->next = prev;
	reverseRecursionD(nxt, curr, head);
}

void reverseRecursion(){
	if(head == NULL || head->next == NULL)
		return;
	reverseRecursionD(*head, NULL, head);
	head = prev;
}
*/
int main(){
	insertAtTheEnd(1);
	insertAtTheEnd(2);
	insertAtTheEnd(3);
	insertAtTheEnd(4);
	insertAtTheEnd(5);
	insertAtTheBeginning(10);
	insertAtTheBeginning(20);
	printTheList();
	reverse();
	printTheList();
	//reverseRecursion();
	printTheList();
	//assert(0);
	return 0;

}