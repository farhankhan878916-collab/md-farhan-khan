package com.example.movieticketbooking.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "customers")
public class Customer extends User {

    @Column(name = "loyalty_points")
    private Integer loyaltyPoints = 0;

    @Column(name = "preferred_city", length = 50)
    private String preferredCity;

    public Customer() {
        super();
        this.setRole(Role.ROLE_CUSTOMER);
    }

    public Customer(String username, String email, String password, String fullName, String phone) {
        super(username, email, password, fullName, phone, Role.ROLE_CUSTOMER);
        this.loyaltyPoints = 0;
    }

    public Customer(String username, String email, String password, String fullName, String phone, String preferredCity) {
        super(username, email, password, fullName, phone, Role.ROLE_CUSTOMER);
        this.loyaltyPoints = 0;
        this.preferredCity = preferredCity;
    }

    @Override
    public String getDisplayRole() {
        return "Customer";
    }

    @Override
    public int getMaxAllowedBookingsPerDay() {
        return 10;
    }

    public Integer getLoyaltyPoints() {
        return loyaltyPoints != null ? loyaltyPoints : 0;
    }

    public void setLoyaltyPoints(Integer loyaltyPoints) {
        this.loyaltyPoints = loyaltyPoints;
    }

    public void addLoyaltyPoints(int points) {
        this.loyaltyPoints = getLoyaltyPoints() + points;
    }

    public String getPreferredCity() {
        return preferredCity;
    }

    public void setPreferredCity(String preferredCity) {
        this.preferredCity = preferredCity;
    }
}
