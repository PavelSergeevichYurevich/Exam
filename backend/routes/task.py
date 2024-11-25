from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from models.models import OrderItem
from dependencies.dependency import get_db
from models.models import Order
from schemas.schemas import AddingItemSchema, DeletingItemSchema, OrderCreateSchema, OrderItemSchema, UpdatingItemSchema


task_router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)
templates = Jinja2Templates(directory="templates")

@task_router.get("/show/")
async def get_items(request:Request, customer_id:int, db: Session = Depends(get_db)):
    stmnt = select(Order).where(Order.customer_id == customer_id)
    orders:list = db.scalars(stmnt).all()
    for order in orders:
        print(order.item)
    return orders

@task_router.post("/add/")
async def add_order(request:Request, order: OrderCreateSchema, order_item: List[OrderItemSchema], db: Session = Depends(get_db)):
    new_order = Order(
        customer_id = order.customer_id, 
        status = order.status,
        )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    for item in order_item:
        new_order_item = OrderItem(
            order_id = new_order.id,
            item_id = item.item_id,
            quantity = item.quantity
        )
        db.add(new_order_item)
        db.commit()
        db.refresh(new_order_item)
    # return RedirectResponse(url="/app/login/", status_code=status.HTTP_302_FOUND)
    return new_order

@task_router.delete(path='/delete/')
async def del_order(request:Request, id:int, db: Session = Depends(get_db)):
    stmnt = delete(Order).where(Order.id == id)
    order = db.execute(stmnt)
    db.commit()
    return order

@task_router.put(path='/update/')
async def update_order(request:Request, updating_item: UpdatingItemSchema, db: Session = Depends(get_db)):
    stmnt = update(OrderItem).where((OrderItem.order_id == updating_item.order_id) & (OrderItem.item_id == updating_item.item_id)).values(
        quantity = updating_item.new_quantity
    )
    updated_item = db.execute(stmnt)
    db.commit()
    return updated_item







    
