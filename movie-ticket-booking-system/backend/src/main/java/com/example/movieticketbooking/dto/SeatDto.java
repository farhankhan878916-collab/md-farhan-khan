package com.example.movieticketbooking.dto;

import java.math.BigDecimal;

public class SeatDto {
    private Long id;
    private String rowName;
    private Integer seatNumber;
    private String seatType; // REGULAR, PREMIUM, VIP
    private BigDecimal price;
    private String status; // AVAILABLE, SELECTED, BOOKED, BLOCKED
    private String seatIdentifier; // e.g., "C5"
    private int rowIndex;
    private int columnIndex;

    public SeatDto() {}

    public SeatDto(Long id, String rowName, Integer seatNumber, String seatType, BigDecimal price, String status) {
        this.id = id;
        this.rowName = rowName;
        this.seatNumber = seatNumber;
        this.seatType = seatType;
        this.price = price;
        this.status = status;
        this.seatIdentifier = rowName + seatNumber;
        this.rowIndex = !rowName.isEmpty() ? (rowName.toUpperCase().charAt(0) - 'A') : 0;
        this.columnIndex = seatNumber != null ? seatNumber - 1 : 0;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRowName() {
        return rowName;
    }

    public void setRowName(String rowName) {
        this.rowName = rowName;
        this.seatIdentifier = (rowName != null ? rowName : "") + (seatNumber != null ? seatNumber : "");
        if (rowName != null && !rowName.isEmpty()) {
            this.rowIndex = rowName.toUpperCase().charAt(0) - 'A';
        }
    }

    public Integer getSeatNumber() {
        return seatNumber;
    }

    public void setSeatNumber(Integer seatNumber) {
        this.seatNumber = seatNumber;
        this.seatIdentifier = (rowName != null ? rowName : "") + (seatNumber != null ? seatNumber : "");
        if (seatNumber != null) {
            this.columnIndex = seatNumber - 1;
        }
    }

    public String getSeatType() {
        return seatType;
    }

    public void setSeatType(String seatType) {
        this.seatType = seatType;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getSeatIdentifier() {
        return seatIdentifier;
    }

    public void setSeatIdentifier(String seatIdentifier) {
        this.seatIdentifier = seatIdentifier;
    }

    public int getRowIndex() {
        return rowIndex;
    }

    public void setRowIndex(int rowIndex) {
        this.rowIndex = rowIndex;
    }

    public int getColumnIndex() {
        return columnIndex;
    }

    public void setColumnIndex(int columnIndex) {
        this.columnIndex = columnIndex;
    }
}
